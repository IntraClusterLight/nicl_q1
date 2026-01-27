#!/gpfs01/home/ppzsb1/.conda/envs/icl/bin/python
# fmt: off
#SBATCH --partition=defq
#SBATCH --cpus-per-task=4
#SBATCH --mem=64g
#SBATCH --time=6:00:00
#SBATCH --job-name=skypatch_stack
#SBATCH --output=logs/%x_%j.out
# fmt: on

"""Stack Q1 skypatch observations."""

import argparse

import astropy.units as u
from astropy.coordinates import SkyCoord

from nicl import configure_logging
from nicl.euclid.combine import combine
from nicl.euclid.data_access import DataAccess
from nicl.euclid.utilities import default_data_path

cutout_size = 2.5 * u.deg
# Number of threads/cores to use for swarp, if not specified swarp will spawn 96 threads! (cores in a compute node)
# maintain consistency with number of cores assigned to the slurm script
nthreads = 4


def combine_vis(ra, dec, name, out_dir, variant="standard", n_eqn_per_img=None):
    cutout_cen = SkyCoord(ra, dec, unit=u.deg)
    bkg_match = True
    autodark_corr = True
    if variant == "no_processing":
        bkg_match = False
        autodark_corr = False
    combine(
        in_dir=default_data_path("Q1_R1", "VIS_QUAD"),
        out_dir=out_dir,
        filters="I",
        cutout_cen=cutout_cen,
        cutout_size=cutout_size,
        bkg_sub=False,
        bkg_match=bkg_match,
        autodark_corr=autodark_corr,
        autodark_dir=default_data_path("Q1_R1_processed_v0.7", "skyflat"),
        name=name,
        pixel_scale=0.3,
        overwrite=True,
        nthreads=nthreads,
        n_eqn_per_img=n_eqn_per_img,
    )


def combine_nir(ra, dec, name, out_dir, filter, variant="standard", n_eqn_per_img=None):
    cutout_cen = SkyCoord(ra, dec, unit=u.deg)
    bkg_match = True
    if variant == "no_processing":
        in_dir = default_data_path("Q1_R1")
        bkg_match = False
    else:
        in_dir = default_data_path("Q1_R1_processed_v0.7", "persistence")
    combine(
        in_dir=in_dir,
        out_dir=out_dir,
        filters=filter,
        bkg_sub=False,
        bkg_match=bkg_match,
        pixel_scale=0.3,
        cutout_cen=cutout_cen,
        cutout_size=cutout_size,
        name=name,
        nthreads=nthreads,
        overwrite=True,
        n_eqn_per_img=n_eqn_per_img,
    )


def combine_mer(ra, dec, name, out_dir, filter):
    cutout_cen = SkyCoord(ra, dec, unit=u.deg)
    mer_filter = dict(I="VIS", Y="NIR-Y", J="NIR-J", H="NIR-H")[filter]
    instrument = "VIS" if mer_filter == "VIS" else "NISP"
    da = DataAccess(release_name="Q1_R1")
    outpath = default_data_path("Q1_R1")
    for mer_file_type in ("STK", "BKG"):
        da.download_files_for_target(
            ra,
            dec,
            radius=cutout_size,
            fully_contained=False,
            instrument=instrument,
            outpath=outpath,
            file_type="MER",
            mer_file_type=mer_file_type,
        )
    combine(
        in_dir=default_data_path("Q1_R1", "MER"),
        out_dir=out_dir,
        filters=mer_filter,
        add_bkg_mod=True,
        cutout_cen=cutout_cen,
        cutout_size=cutout_size,
        name=name,
        pixel_scale=0.3,
        overwrite=True,
        nthreads=nthreads,
    )


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    configure_logging(name="nicl.mask", level="WARNING")
    configure_logging(name="nicl.euclid.continuity", level="INFO")
    parser = argparse.ArgumentParser(
        description="Process Q1 skypatch stacks for a specified filter and processing variant."
    )
    parser.add_argument(
        "field",
        type=str,
        choices=["EDFS", "EDFF", "EDFN"],
        help="Field of the skypatch to be processed.",
    )
    parser.add_argument(
        "filter",
        type=str,
        choices=["I", "Y", "J", "H"],
        help="Filter of the stacks to be processed.",
    )
    parser.add_argument(
        "variant",
        type=str,
        choices=[
            "standard",
            "no_processing",
            "mer",
        ],
        default="standard",
        help="Variant of the data processing to be stacked.",
    )
    parser.add_argument(
        "--n_eqn_per_img",
        type=int,
        default=None,
        help="Target number of equations per image for background matching.",
    )

    args = parser.parse_args()
    out_dir = args.variant
    if args.n_eqn_per_img is not None:
        out_dir += f"_n_eqn_per_img_{args.n_eqn_per_img}"
    out_dir = default_data_path("Q1_R1_clusters_v1.0/skypatch", out_dir)
    name = f"{args.field}_sky"
    if args.field == "EDFN":
        ra = 270.0 * u.deg
        dec = 66.0 * u.deg
    elif args.field == "EDFS":
        ra = 58.5 * u.deg
        dec = -49.5 * u.deg
    elif args.field == "EDFF":
        ra = 53.0 * u.deg
        dec = -28.0 * u.deg
    if args.filter in ["Y", "J", "H"]:
        if args.variant == "mer":
            combine_mer(ra, dec, name, out_dir, args.filter)
        else:
            combine_nir(
                ra,
                dec,
                name,
                out_dir,
                args.filter,
                variant=args.variant,
                n_eqn_per_img=args.n_eqn_per_img,
            )
    elif args.filter == "I":
        if args.variant == "mer":
            combine_mer(ra, dec, name, out_dir, args.filter)
        else:
            combine_vis(
                ra,
                dec,
                name,
                out_dir,
                variant=args.variant,
                n_eqn_per_img=args.n_eqn_per_img,
            )
