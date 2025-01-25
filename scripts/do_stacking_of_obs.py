"""Perform stacking for all of Q1 in the default location."""

from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import os

from nicl.euclid.data_access import DataAccess
from nicl.euclid.combine import combine
from nicl.euclid.utilities import default_data_path

def try_combine(*args, **kwargs):
    obs_id = kwargs["obs_ids"]
    try:
        print(f"Processing {obs_id}...", flush=True)
        combine(*args, **kwargs)
        print(f"Completed {obs_id}...", flush=True)
    except Exception as e:
        print("Exception in combine:", e)
        
def main(max_workers=1, release_name="Q1_R1", input_folder="Q1_R1_processed_v0.4/persistence/NIR/"):
    print(f"{os.cpu_count()} CPUs available, using {max_workers}.")
    da = DataAccess(release_name=release_name)
    in_path = default_data_path(input_folder)
    out_path = default_data_path(f"{release_name}_processed_v0.4/")
    obs_ids = da.find_all_observations()
    obs_ids = sorted(obs_ids)
    obs_ids = [2682]
    print(f"All {len(obs_ids)} obs_ids to process:")
    print(obs_ids)
    print("Processing:")
    if max_workers > 1:
        # running in parallel may cause errors in swarp
        # to be checked if using "spawn" resolves this
        mp_context = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(mp_context=mp_context, max_workers=max_workers) as executor:
            for obs_id in obs_ids:
                #executor.submit(try_combine, obs_ids=obs_id, in_dir=in_path, out_dir=out_path / f"stacked_original/NIR/{obs_id}", bkg_sub=True)
                #executor.submit(try_combine, obs_ids=obs_id, in_dir=in_path, out_dir=out_path / f"stacked/NIR/{obs_id}", bkg_sub=True)
                executor.submit(try_combine, obs_ids=obs_id, in_dir=in_path, out_dir=out_path / f"stacked_no_bkg/NIR/{obs_id}", bkg_sub=False)
    else:
        for obs_id in obs_ids:
            #try_combine(obs_ids=obs_id, in_dir=in_path, out_dir=out_path / f"stacked_original/NIR/{obs_id}", bkg_sub=True)
            #try_combine(obs_ids=obs_id, in_dir=in_path, out_dir=out_path / f"stacked/NIR/{obs_id}", bkg_sub=True)
            try_combine(obs_ids=obs_id, in_dir=in_path, out_dir=out_path / f"stacked_no_bkg/NIR/{obs_id}", bkg_sub=False)
                
if __name__ == '__main__':
    main(max_workers=1)
