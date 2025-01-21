"""Download all the NIR files for Q1 to the default location."""

import sys

from nicl.euclid.data_access import DataAccess
from nicl.euclid.utilities import default_data_path

release_name = "Q1_R1"
da = DataAccess(release_name=release_name)
outpath = default_data_path(release_name)
print(f"Saving data to {outpath}")
obs_ids = da.find_all_observations()
print(f"All {len(obs_ids)} obs_ids to download:")
print(obs_ids)
print("Downloading:")
for obs_id in obs_ids:
    print(obs_id, flush=True)
    da.download_calibrated_files_for_observation(obs_id, instrument="NISP", outpath=outpath)
