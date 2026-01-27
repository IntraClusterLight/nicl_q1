#!/gpfs01/home/ppzsb1/.conda/envs/icl/bin/python
# fmt: off
#SBATCH --partition=defq
#SBATCH --cpus-per-task=2
#SBATCH --mem=32g
#SBATCH --time=3:00:00
#SBATCH --array=1-15
#SBATCH --output=logs/%x_%A_%a.out
# fmt: on

import argparse
import logging
import os

from nicl import configure_logging
from nicl.autoprof import create_bkgsub_clean_images
from nicl.euclid.mask import ICL_BKG_FILTER_SIZE
from nicl.euclid.skypatch_noise import measure_noise_in_apertures
from nicl.euclid.utilities import default_data_path

mer_equivalent = int(256 * 0.1 / 0.3)
box_sizes = [mer_equivalent]
box_sizes += [450, 500, 550, 650, 750, 1000, 1800, 2350]
box_sizes += [300, 850, 1250, 1500, 2000, 2750]

nir_stack_bkg_box_size = 3000

if __name__ == "__main__":
    configure_logging(level="DEBUG")
    configure_logging(name="nicl.mask", level="INFO")
    log = logging.getLogger(__name__)
    log.setLevel("DEBUG")

    task_id = os.getenv("SLURM_ARRAY_TASK_ID")
    parser = argparse.ArgumentParser()
    parser.add_argument("field", type=str)
    parser.add_argument("band", type=str)
    parser.add_argument("variant", type=str)
    parser.add_argument("--boxes", action="store_true")
    if task_id is None:
        parser.add_argument("box_size", type=int)
        args = parser.parse_args()
        box_size = args.box_size
    else:
        args = parser.parse_args()
        task_id = int(task_id)
        box_size = box_sizes[task_id - 1]

    aperture_type = "boxes" if args.boxes else "annuli"

    data_dir = default_data_path("Q1_R1_clusters_v1.0", "skypatch", args.variant)
    output_field_dir = default_data_path(
        "Q1_R1_clusters_v1.0_measurements", "skypatch", args.field
    )
    output_variant_dir = output_field_dir / "new" / args.variant
    output_variant_dir.mkdir(parents=True, exist_ok=True)

    prefix = f"{args.field}_Skypatch_bs{box_size}"
    tmp_dir = output_variant_dir / "tmp" / aperture_type / prefix
    cleaned_dir = tmp_dir / "cleaned"
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    log.info(
        f"Measuring noise in {aperture_type} in {args.field} for band {args.band} with box size {box_size}."
    )

    image_paths = {
        "H": next(data_dir.glob(f"EUC*H?{args.field}_sky.fits"), None),
        "J": next(data_dir.glob(f"EUC*J?{args.field}_sky.fits"), None),
        "Y": next(data_dir.glob(f"EUC*Y?{args.field}_sky.fits"), None),
        "VIS": next(data_dir.glob(f"EUC*VIS*{args.field}_sky.fits"), None),
        "YJH": output_field_dir / f"{args.field}_YJH.fits",
    }

    if args.band == "YJH":
        mask_path = output_field_dir / f"{args.field}_YJH_measurement_mask.fits"
    elif args.band in ["H", "J", "Y"]:
        mask_path = output_field_dir / f"{args.field}_YJH_measurement_mask.fits"
    elif args.band == "VIS":
        mask_path = output_field_dir / f"{args.field}_VIS_measurement_mask.fits"

    log.info("Creating background subtracted image.")
    cleaned_filename = create_bkgsub_clean_images(
        image_filenames=image_paths[args.band],
        output_dir=cleaned_dir,
        mask_filename=mask_path,
        output_background_dir=None,
        box_size=box_size,
        filter_size=ICL_BKG_FILTER_SIZE,
    )

    if args.variant == "mer":
        mer_zp = {"VIS": 24.6, "Y": 29.8, "J": 30.0, "H": 29.9}
        zp = mer_zp[args.band]
    else:
        zp = 23.9

    log.info(f"Measuring noise in {aperture_type}.")
    measure_noise_in_apertures(
        image_path=cleaned_filename,
        mask_path=mask_path,
        aperture_type=aperture_type,
        num_points=1000,
        pixelscale=0.3,
        output_path=output_variant_dir,
        label=f"{prefix}_{args.band}",
        plot_overlay=False,
        save_diagnostics=(not args.boxes),
        zp=zp,
    )

    cleaned_filename.unlink()
    log.info("Completed.")
