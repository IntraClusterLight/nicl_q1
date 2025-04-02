"""Perform stacking for the 4 test clusters."""

import pandas as pd

from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord

from nicl.euclid.combine import combine
from nicl.euclid.utilities import default_data_path

def try_combine(*args, **kwargs):
    name = kwargs["name"]
    try:
        print(f"Processing {name}...", flush=True)
        combine(*args, **kwargs)
        print(f"Completed {name}...", flush=True)
    except Exception as e:
        print("Exception in combine:", e)


def main():
    clusters = pd.read_csv(default_data_path("catalogs") / "Subset_Q1Clusters.csv")
    in_path = default_data_path("Q1_R1_processed_v0.7", "persistence")
    out_path = default_data_path("Q1_R1_clusters_v0.7", "tutku")
    for cluster in clusters.itertuples():
        cutout_cen = SkyCoord(cluster.RA * u.deg, cluster.DEC * u.deg, frame="icrs")
        cutout_size = 2 * cluster.R_deg * u.deg
        try_combine(name=cluster.ID, cutout_cen=cutout_cen, cutout_size=cutout_size,
                    in_dir=in_path, out_dir=out_path, pixel_scale=0.3, bkg_sub=True)
    for cluster in clusters.itertuples():
        cutout_cen = SkyCoord(cluster.RA * u.deg, cluster.DEC * u.deg, frame="icrs")
        cutout_size = 2 * cluster.R_deg * u.deg
        try_combine(name=f"{cluster.ID}_no_bkg", cutout_cen=cutout_cen, cutout_size=cutout_size,
                    in_dir=in_path, out_dir=out_path, pixel_scale=0.3, bkg_sub=False)

if __name__ == '__main__':
    main()
