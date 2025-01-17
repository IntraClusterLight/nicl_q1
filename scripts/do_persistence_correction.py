"""Perform persistence correction for all of Q1 in the default location."""

from concurrent.futures import ProcessPoolExecutor
import os
import sys

from nicl.euclid.data_access import DataAccess
from nicl.euclid.persistence import correct_persistence
from nicl.euclid.utilities import default_data_path

def try_correct_persistence(*args, **kwargs):
    try:
        correct_persistence(*args, **kwargs)
    except Exception as e:
        print(e)
        
def main(max_workers=1, release_name="Q1_R1", processed_version="v0.4"):
    print(f"{os.cpu_count()} CPUs available, using {max_workers}.")
    da = DataAccess(release_name=release_name)
    path = default_data_path(release_name)
    processed_path = default_data_path(f"{release_name}_processed_{processed_version}")
    obs_ids = da.find_all_observations()
    print(f"All {len(obs_ids)} obs_ids to process:")
    print(obs_ids)
    print("Processing:")
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for obs_id in obs_ids:
            outpath = processed_path / f"persistence/NIR/{obs_id}/"
            skyflat_path = processed_path / f"skyflat/skyflats/NIR/{obs_id}/"
            executor.submit(try_correct_persistence, obs_id, path, outpath=outpath, skyflat_path=skyflat_path)

if __name__ == '__main__':
    main(max_workers=4)
