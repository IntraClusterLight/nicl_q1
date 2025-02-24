"""Download all the MER files for Erosita clusters in Q1 to the default location."""

import sys

import pandas as pd
from astropy import units as u
from nicl.euclid.data_access import DataAccess
from nicl.euclid.utilities import default_data_path

release_name = "Q1_R1"
da = DataAccess(release_name=release_name)
outpath = default_data_path(release_name)
print(f"Saving data to {outpath}")

df = pd.read_csv(outpath / "../catalogs/Erosita_2E14.csv")

for cluster in df.itertuples():
    print(cluster.ID)
    for mer_file_type in ("STK", "BKG"):
        da.download_files_for_target(cluster.RA,
                                     cluster.DEC,
                                     cluster.R_deg * u.deg,
                                     fully_contained=False,
                                     outpath=outpath,
                                     instrument="VIS",
                                     file_type="MER",
                                     mer_file_type=mer_file_type)