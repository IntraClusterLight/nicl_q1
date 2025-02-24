from nicl.euclid.skyflat import create_skyflats, group_obs_ids, write_skyflats
from nicl.euclid.utilities import default_data_path
from nicl.euclid.xarray import create_all_zarr_refs, read_all_zarr_refs

path = default_data_path("Q1_R1", "NIR")
zarr_path = default_data_path("zarr", "Q1_R1", "NIR")
outpath = default_data_path("Q1_R1_processed_v0.4", "skyflat", "NIR")

n_pix = 51
half_window = 3
create_all_zarr_refs(path, zarr_path)
ds, wcs, zp = read_all_zarr_refs(zarr_path)
obs_ids = sorted(ds.observation_id.values)
group_for_obs_id = group_obs_ids(obs_ids, half_window=half_window)

for obs_id in obs_ids:
    if len(list(outpath.glob(f"flat-{obs_id}-*.fits"))) > 0:
        print(f"Skipping {obs_id} because it already exists")
        continue
    print("Creating skyflats for obs_id:", obs_id, flush=True)
    print("Using obs_ids:", group_for_obs_id[obs_id], flush=True)
    flats = create_skyflats(obs_id, group_for_obs_id, zarr_path, n_pix=n_pix)
    write_skyflats(obs_id, flats, outpath, wcs)
