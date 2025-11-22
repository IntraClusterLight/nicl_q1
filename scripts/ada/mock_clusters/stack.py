"""Stack Q1 Mock Cluster observations."""

import argparse
import logging

import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.table import Table

from nicl import configure_logging
from nicl.euclid.combine import combine
from nicl.euclid.utilities import default_data_path

cutout_size = 30 * u.arcmin
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
        in_dir=default_data_path("Q1_R1_mock_clusters", "VIS_QUAD"),
        out_dir=out_dir,
        filters="I",
        cutout_cen=cutout_cen,
        cutout_size=cutout_size,
        bkg_sub=(not autodark_corr),
        bkg_mesh_size=cutout_size,
        bkg_filter_size=1,
        bkg_match=bkg_match,
        autodark_corr=autodark_corr,
        autodark_dir=default_data_path("Q1_R1_mock_clusters_processed_v1.0", "skyflat"),
        name=name,
        pixel_scale=0.3,
        overwrite=True,
        nthreads=nthreads,
        recurse_symlinks=False,
    )


def combine_nir(ra, dec, name, out_dir, filter, variant="standard"):
    cutout_cen = SkyCoord(ra, dec, unit=u.deg)
    bkg_match = True
    bkg_sub = False
    if variant == "no_processing":
        in_dir = default_data_path("Q1_R1_mock_clusters")
        bkg_match = False
        bkg_sub = True
    else:
        in_dir = default_data_path("Q1_R1_mock_clusters_processed_v1.0")
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
        recurse_symlinks=False,
    )


if __name__ == "__main__":
    configure_logging(level="DEBUG")
    # configure_logging(name="nicl.mask", level="WARNING")
    log = logging.getLogger(__name__)
    log.setLevel("INFO")
    parser = argparse.ArgumentParser(
        description="Process Q1 mock cluster stacks for row TASK_ID from PARAM_TABLE."
    )
    parser.add_argument(
        "param_table", help="Path to table file of name, ra and dec of the clusters."
    )
    parser.add_argument(
        "subfolder", type=str, help="Subfolder to save the output stacks in."
    )
    parser.add_argument(
        "filter",
        type=str,
        choices=["I", "Y", "J", "H"],
        help="Filter of the stacks to be processed.",
    )
    parser.add_argument(
        "--variant",
        type=str,
        choices=[
            "standard",
            "no_persistence",
            "no_skyflat",
            "no_tartan",
            "no_processing",
            "no_bkg_match",
        ],
        default="standard",
        help="Variant of the data processing to be stacked.",
    )
    parser.add_argument(
        "task_id",
        type=int,
        help="SLURM_ARRAY_TASK_ID (1-based index into param_table rows).",
    )

    args = parser.parse_args()
    table_path = args.param_table
    task_id = args.task_id
    sample = Table.read(table_path, format="ascii")
    out_dir = default_data_path(
        "Q1_R1_mock_clusters_v1.0", args.subfolder, args.variant
    )
    if task_id <= len(sample):
        row = sample[task_id - 1]  # SLURM_ARRAY_TASK_ID is 1-based
        name = str(row[0])
        ra = row[1]
        dec = row[2]
        log.info(
            f"Stacking mock cluster {name} in filter {args.filter} for variant {args.variant} (task ID {task_id})"
        )
        if args.filter in ["Y", "J", "H"]:
            combine_nir(ra, dec, name, out_dir, args.filter, variant=args.variant)
        elif args.filter == "I":
            combine_vis(ra, dec, name, out_dir, variant=args.variant)
    else:
        log.warning(
            f"Task ID {task_id} exceeds the number of rows in the table ({len(sample)})."
        )
