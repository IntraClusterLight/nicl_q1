"""Get Q1 VIS data for Nina's EDFN test clusters."""

import sys

from astropy.table import Table
from astropy import units as u

from nicl.euclid.data_access import DataAccess
from nicl.euclid.utilities import default_data_path

release_name = "Q1_R1"
da = DataAccess(release_name=release_name)
outpath = default_data_path(release_name)
print(f"Saving data to {outpath}")

clusters = Table.read(default_data_path("catalogs/EDFN_CLUSTERS_LSB_processing_subset.fits"))
for cluster in clusters:
    print(cluster["Name"], flush=True)
    for instrument in ("VIS",):
        da.download_files_for_target(cluster["RA"],
                                     cluster["DEC"],
                                     0.5 * cluster["boxsize"] * u.arcmin,
                                     fully_contained=False,
                                     outpath=outpath,
                                     instrument=instrument,
                                     file_type="CAL")
        sys.stdout.flush()
        for mer_file_type in ("STK", "BKG"):
            da.download_files_for_target(cluster["RA"],
                                         cluster["DEC"],
                                         0.5 * cluster["boxsize"] * u.arcmin,
                                         fully_contained=False,
                                         outpath=outpath,
                                         instrument=instrument,
                                         file_type="MER",
                                         mer_file_type=mer_file_type)
            sys.stdout.flush()
