"""Download all the MER files for DES clusters in Q1 to the default location."""

import sys

import pandas as pd
from astropy import units as u
from nicl.euclid.data_access import DataAccess
from nicl.euclid.utilities import default_data_path

release_name = "Q1_R1"
da = DataAccess(release_name=release_name)
outpath = default_data_path(release_name)
print(f"Saving data to {outpath}")

df = pd.read_csv(outpath / "../catalogs/Euclid_Q1_DES_JGM.csv")

for cluster in df.itertuples():
    print(cluster.ID)
    for instrument in ("VIS",):
        for mer_file_type in ("STK", "BKG"):
            da.download_files_for_target(cluster.RA,
                                         cluster.Dec,
                                         0.5 * cluster.ImageSize * u.deg,
                                         fully_contained=False,
                                         outpath=outpath,
                                         instrument=instrument,
                                         file_type="MER",
                                         mer_file_type=mer_file_type)
            sys.stdout.flush()
