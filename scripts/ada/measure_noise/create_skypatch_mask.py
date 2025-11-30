#!/gpfs01/home/ppzsb1/.conda/envs/icl/bin/python
# fmt: off
#SBATCH --partition=defq
#SBATCH --cpus-per-task=2
#SBATCH --mem=64g
#SBATCH --time=1:00:00
#SBATCH --output=logs/%x_%j.out
# fmt: on

import argparse
import logging
import shutil

from nicl import configure_logging
from nicl.euclid.mask import (
    create_combined_nir_mask,
    create_vis_mask,
)
from nicl.euclid.utilities import default_data_path

nir_stack_bkg_box_size = 3000

if __name__ == "__main__":
    configure_logging(level="DEBUG")
    configure_logging(name="nicl.mask", level="INFO")
    log = logging.getLogger(__name__)
    log.setLevel("DEBUG")

    parser = argparse.ArgumentParser()
    parser.add_argument("field", type=str)
    parser.add_argument("band", type=str)
    args = parser.parse_args()
    field = args.field
    band = args.band

    data_dir = default_data_path("Q1_R1_clusters_v1.0", "skypatch")
    output_dir = default_data_path(
        "Q1_R1_clusters_v1.0_measurements", "skypatch", field
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    log.info(f"Creating NIR mask for {field} and band {band}.")

    image_paths = {
        "H": data_dir / f"EUC_NIR_W-STK_H-{field}_sky.fits",
        "J": data_dir / f"EUC_NIR_W-STK_J-{field}_sky.fits",
        "Y": data_dir / f"EUC_NIR_W-STK_Y-{field}_sky.fits",
        "VIS": data_dir / f"EUC_VIS_SWL-STK-{field}_sky.fits",
        "YJH": output_dir / f"{field}_YJH.fits",
    }

    if band == "YJH":
        mask_path = output_dir / f"{field}_YJH_measurement_mask.fits"
        if not mask_path.exists():
            log.info(f"Creating NIR mask using box size {nir_stack_bkg_box_size}.")
            create_combined_nir_mask(
                image_paths["H"],
                image_paths["J"],
                image_paths["Y"],
                centre_pos=False,  # indicates that this is not a cluster image
                label=field,
                output_dir=output_dir,
                nir_stack_bkg_box_size=nir_stack_bkg_box_size,
            )
            log.info("Created NIR mask.")
        else:
            log.info("NIR mask already exists.")
    elif band == "VIS":
        mask_path = output_dir / f"{field}_VIS_measurement_mask.fits"
        if not mask_path.exists():
            log.info("Creating VIS mask.")
            create_vis_mask(
                image_paths["VIS"],
                centre_pos=False,
                label=field,
                output_dir=output_dir,
            )
            log.info("Created VIS mask.")
        else:
            log.info("VIS mask already exists.")

    if band == "YJH":
        shutil.rmtree(output_dir / "tmp")
    log.info("Completed.")
