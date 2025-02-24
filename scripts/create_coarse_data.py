from nicl.euclid.skyflat import create_coarse_data
from nicl.euclid.utilities import default_data_path
from nicl.euclid.xarray import read_all_zarr_refs

zarr_path = default_data_path("zarr", "Q1_R1", "NIR")

n_pix = 51
ds, wcs, zp = read_all_zarr_refs(zarr_path)
obs_ids = sorted(ds.observation_id.values)

for obs_id in obs_ids:
    print(obs_id, flush=True)
    create_coarse_data(obs_id, zarr_path, n_pix=n_pix)
