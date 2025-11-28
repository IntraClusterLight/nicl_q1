#!/gpfs01/home/ppzsb1/.conda/envs/icl/bin/python
# fmt: off
#SBATCH --partition=defq
#SBATCH --cpus-per-task=2
#SBATCH --mem=64g
#SBATCH --time=5:00:00
# #SBATCH --array=1-80
#SBATCH --output=logs/%x_%j.out
# fmt: on

import argparse
import itertools
import logging
import os

from nicl import configure_logging
from nicl.autoprof import create_bkgsub_clean_images
from nicl.euclid.mask import (
    create_combined_nir_mask,
    create_vis_mask,
    NIR_STACK_BKG_FILTER_SIZE,
)
from nicl.euclid.skypatch_noise import measure_noise_in_circular_annuli
from nicl.euclid.utilities import default_data_path

fields = ["EDFS", "EDFF"]
box_sizes = [450, 500, 550, 650, 750, 1000, 1800, 2350]
bands = ["VIS", "H", "J", "Y", "YJH"]

if __name__ == "__main__":
    configure_logging(level="DEBUG")
    configure_logging(name="nicl.mask", level="WARNING")
    log = logging.getLogger(__name__)
    log.setLevel("DEBUG")

    task_id = os.getenv("SLURM_ARRAY_TASK_ID")
    if task_id is None:
        parser = argparse.ArgumentParser()
        parser.add_argument("field", type=str)
        parser.add_argument("box_size", type=int)
        parser.add_argument("band", type=str)
        args = parser.parse_args()
        field = args.field
        box_size = args.box_size
        band = args.band
    else:
        task_id = int(task_id)
        tasks = list(itertools.product(fields, box_sizes, bands))
        field, box_size, band = tasks[task_id - 1]

    data_dir = default_data_path("Q1_R1_clusters_v1.0", "skypatch")
    output_dir = default_data_path("Q1_R1_clusters_v1.0_measurements", "skypatch")
    output_dir.mkdir(parents=True, exist_ok=True)

    temp_dir = output_dir / "temp_cleaned"
    temp_dir.mkdir(exist_ok=True)
    prefix = f"{field}_Skypatch_bs{box_size}"
    log.info(f"Measuring noise in {field} for band {band} with box size {box_size}")

    image_paths = {
        "H": data_dir / f"EUC_NIR_W-STK_H-{field}_sky.fits",
        "J": data_dir / f"EUC_NIR_W-STK_J-{field}_sky.fits",
        "Y": data_dir / f"EUC_NIR_W-STK_Y-{field}_sky.fits",
        "VIS": data_dir / f"EUC_VIS_SWL-STK-{field}_sky.fits",
        "YJH": output_dir / f"{prefix}_YJH.fits",
    }

    if band == "YJH":
        mask_path = output_dir / f"{field}_YJH_measurement_mask.fits"
        if not mask_path.exists():
            log.info("Creating NIR mask")
            create_combined_nir_mask(
                image_paths["H"],
                image_paths["J"],
                image_paths["Y"],
                centre_pos=False,  # indicates that this is not a cluster image
                label=field,
                output_dir=output_dir,
                nir_stack_bkg_box_size=500,
            )
            log.info("Created NIR mask.")
        else:
            log.info("NIR mask already exists.")
    elif band in ["H", "J", "Y"]:
        mask_path = output_dir / f"{field}_YJH_measurement_mask.fits"
        if not mask_path.exists():
            OSError("Run YJH first to create NIR mask.")
    elif band == "VIS":
        mask_path = output_dir / f"{field}_VIS_measurement_mask.fits"
        if not mask_path.exists():
            log.info("Creating VIS mask")
            create_vis_mask(
                image_paths["VIS"],
                centre_pos=False,
                label=field,
                output_dir=output_dir,
            )
            log.info("Created VIS mask.")
        else:
            log.info("VIS mask already exists.")

    log.info("Creating background subtracted image")
    cleaned_filename = create_bkgsub_clean_images(
        image_filenames=image_paths[band],
        output_dir=temp_dir,
        mask_filename=mask_path,
        output_background_dir=output_dir,
        box_size=box_size,
        filter_size=NIR_STACK_BKG_FILTER_SIZE,
    )

    log.info("Measuring noise in circular annuli")
    measure_noise_in_circular_annuli(
        image_path=cleaned_filename,
        mask_path=mask_path,
        num_points=10,
        pixelscale=0.3,
        output_path=output_dir,
        label=f"{prefix}_{band}",
        plot_annuli=False,
        save_diagnostics=True,
    )

    temp_dir.rmtree()
    log.info("Completed")
