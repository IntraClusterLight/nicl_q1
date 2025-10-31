#!/gpfs01/home/ppzsb1/.conda/envs/icl/bin/python
# fmt: off
#SBATCH --partition=defq
#SBATCH --cpus-per-task=1
#SBATCH --mem=4g
#SBATCH --time=0:20:00
#SBATCH --job-name=illustration_stack
#SBATCH --output=logs/%x_%j.out
# fmt: on

"""Stack Q1 illustration observations."""

import argparse

import astropy.units as u
from astropy.coordinates import SkyCoord

from nicl import configure_logging
from nicl.euclid.combine import combine
from nicl.euclid.data_access import DataAccess
from nicl.euclid.utilities import default_data_path

cutout_size = 11 * u.arcmin
# Number of threads/cores to use for swarp, if not specified swarp will spawn 96 threads! (cores in a compute node)
# maintain consistency with number of cores in the stack_Q1.sh slurm script
nthreads = 1


def combine_vis(ra, dec, name, out_dir, variant="standard"):
    cutout_cen = SkyCoord(ra, dec, unit=u.deg)
    bkg_match = True
    autodark_corr = True
    if variant == "no_processing":
        bkg_match = False
        autodark_corr = False
    elif variant == "no_bkg_match":
        bkg_match = False
    elif variant == "no_skyflat":
        autodark_corr = False
    combine(
        in_dir=default_data_path("Q1_R1", "VIS_QUAD"),
        out_dir=out_dir,
        filters="I",
        cutout_cen=cutout_cen,
        cutout_size=cutout_size,
        bkg_sub=(not autodark_corr),
        bkg_mesh_size=cutout_size,
        bkg_filter_size=1,
        bkg_match=bkg_match,
        autodark_corr=autodark_corr,
        autodark_dir=default_data_path("Q1_R1_processed_v0.7", "skyflat"),
        name=name,
        pixel_scale=0.3,
        overwrite=True,
        nthreads=nthreads,
    )


def combine_nir(ra, dec, name, out_dir, filter, variant="standard"):
    cutout_cen = SkyCoord(ra, dec, unit=u.deg)
    bkg_match = True
    bkg_sub = False
    if variant == "no_processing":
        in_dir = default_data_path("Q1_R1")
        bkg_match = False
        bkg_sub = True
    else:
        in_dir = default_data_path("Q1_R1_processed_illustrations/ablation")
        if variant == "standard":
            in_dir = in_dir / "persistence"
        elif variant == "no_persistence":
            in_dir = in_dir / "no_persistence"
        elif variant == "no_skyflat":
            in_dir = in_dir / "persistence_no_skyflat"
            bkg_sub = True
        elif variant == "no_tartan":
            in_dir = in_dir / "persistence_no_tartan"
        elif variant == "no_bkg_match":
            in_dir = in_dir / "persistence"
            bkg_match = False
    combine(
        in_dir=in_dir,
        out_dir=out_dir,
        filters=filter,
        bkg_sub=bkg_sub,
        bkg_mesh_size=cutout_size,
        bkg_filter_size=1,
        bkg_match=bkg_match,
        pixel_scale=0.3,
        cutout_cen=cutout_cen,
        cutout_size=cutout_size,
        name=name,
        nthreads=nthreads,
        overwrite=True,
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
    parser = argparse.ArgumentParser(
        description="Process Q1 illustration stacks for a specified filter and processing variant."
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
            "no_persistence",
            "no_skyflat",
            "no_tartan",
            "no_processing",
            "no_bkg_match",
            "mer",
        ],
        default="standard",
        help="Variant of the data processing to be stacked.",
    )

    args = parser.parse_args()
    out_dir = default_data_path(
        "Q1_R1_processed_illustrations", "ablation/cluster", args.variant
    )
    name = "MCXCJ1754.6+6803"
    ra = 268.662 * u.deg
    dec = 68.058 * u.deg
    if args.filter in ["Y", "J", "H"]:
        if args.variant == "mer":
            combine_mer(ra, dec, name, out_dir, args.filter)
        else:
            combine_nir(ra, dec, name, out_dir, args.filter, variant=args.variant)
    elif args.filter == "I":
        if args.variant == "mer":
            combine_mer(ra, dec, name, out_dir, args.filter)
        else:
            combine_vis(ra, dec, name, out_dir, variant=args.variant)
