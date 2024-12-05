"""Perform stacking for all of Q1 in the default location."""

from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import os
import sys

from nicl.euclid.data_access import DataAccess
from nicl.euclid.combine import Combiner
from nicl.euclid.utilities import default_data_path

def try_stacking(*args, **kwargs):
    try:
        combiner = Combiner(*args, **kwargs)
        combiner.combine()
    except Exception as e:
        print(e)
        
def main(max_workers=1, release_name="Q1_R1", input_folder="Q1_R1_processed_v0.2/"):
    print(f"{os.cpu_count()} CPUs available, using {max_workers}.")
    da = DataAccess(release_name=release_name)
    in_path = default_data_path(input_folder)
    obs_ids = da.find_all_observations()
    print(f"All {len(obs_ids)} obs_ids to process:")
    print(obs_ids)
    print("Processing:")
    if max_workers > 1:
        # running in parallel may cause errors in swarp
        # to be checked if using "spawn" resolves this
        mp_context = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(mp_context=mp_context, max_workers=max_workers) as executor:
            for obs_id in obs_ids:
                out_path = in_path / f"../Q1_R1_processed_v0.2/stacked/NIR/{obs_id}/"
                executor.submit(try_stacking, obs_ids=obs_id, in_path=in_path, out_path=out_path)
    else:
        for obs_id in obs_ids:
            out_path = in_path / f"../Q1_R1_processed_v0.2/stacked/NIR/{obs_id}/"
            try_stacking(obs_ids=obs_id, in_path=in_path, out_path=out_path)        
                
if __name__ == '__main__':
    main(max_workers=1)
