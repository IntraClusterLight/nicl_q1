"""Download DR1 data in the EDFS."""

from functools import partial

import numpy as np
from astropy.table import Table

from nicl import configure_logging
from nicl.euclid.utilities import default_data_path
from nicl.euclid.pipeline import Pipeline


configure_logging(level="INFO")

release_name = "DR1"

pipeline = partial(
    Pipeline,
    release_name=release_name,
)

tab = Table.read(default_data_path("catalogs") / "EDFS_obs_ids.vot")
obs_ids = np.array(tab["observation_id"], dtype=int)

with pipeline(target_obs_ids=obs_ids) as p:
    p.get_nir_data()
