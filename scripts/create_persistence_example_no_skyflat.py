from nicl.euclid.utilities import default_data_path
from nicl.euclid.persistence import correct_persistence

path = default_data_path("Q1_R1")
obs_id = 2683
skyflat_path = default_data_path("Q1_R1_processed_v0.4/skyflat/NIR/")

outpath = default_data_path(
    f"Q1_R1_processed_test/persistence_no_skyflat/NIR/{obs_id}"
)
correct_persistence(
    obs_id,
    path,
    skyflat_path=skyflat_path,
    outpath=outpath,
    correct_banding=True,
    final_skyflat_correction=False,
    overwrite=True,
)


