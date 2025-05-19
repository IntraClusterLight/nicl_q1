import argparse

import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.table import Table

from nicl.euclid.combine import combine
from nicl.euclid.utilities import default_data_path

cutout_size = 30 * u.arcmin
# Number of threads/cores to use for swarp, if not specified swarp will spawn 96 threads! (cores in a compute node)
# maintain consistency with number of cores in the stack_Q1.sh slurm script
nthreads = 1


def combine_vis(ra, dec, name, out_dir):
    cutout_cen = SkyCoord(ra, dec, unit=u.deg)
    combine(
        in_dir=default_data_path("Q1_R1", "VIS_QUAD"),
        out_dir=out_dir,
        filters="I",
        cutout_cen=cutout_cen,
        cutout_size=cutout_size,
        bkg_sub=False,
        bkg_match=True,
        autodark_corr=True,
        autodark_dir=default_data_path("Q1_R1_processed_v0.7", "skyflat", "VIS"),
        name=name,
        pixel_scale=0.3,
        overwrite=True,
        nthreads=nthreads,
    )


def combine_nir(ra, dec, name, out_dir, filter):
    cutout_cen = SkyCoord(ra, dec, unit=u.deg)
    combine(
        in_dir=default_data_path("Q1_R1_processed_v0.7", "persistence"),
        out_dir=out_dir,
        filters=filter,
        bkg_sub=False,
        bkg_match=True,
        pixel_scale=0.3,
        cutout_cen=cutout_cen,
        cutout_size=cutout_size,
        name=name,
        nthreads=nthreads,
        overwrite=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process Q1 cluster stacks for row TASK_ID from PARAM_TABLE."
    )
    parser.add_argument(
        "param_table", help="Path to table file of ra, dec, and name of the clusters."
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
        "task_id",
        type=int,
        help="SLURM_ARRAY_TASK_ID (1-based index into param_table rows).",
    )

    args = parser.parse_args()
    table_path = args.param_table
    task_id = args.task_id
    sample = Table.read(table_path, format="ascii")
    out_dir = default_data_path("Q1_R1_clusters_v1.0", args.subfolder)
    if task_id <= len(sample):
        row = sample[task_id - 1]  # SLURM_ARRAY_TASK_ID is 1-based
        name = str(row[0])
        ra = row[1]
        dec = row[2]
        if args.filter in ["Y", "J", "H"]:
            combine_nir(ra, dec, name, out_dir, args.filter)
        elif args.filter == "I":
            combine_vis(ra, dec, name, out_dir)
    else:
        print(f"Task ID {task_id} exceeds the number of rows in the table.")
        print(f"Total rows in table: {len(sample)}")
