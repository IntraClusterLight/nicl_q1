from functools import partial

from nicl.euclid.data_access import DataAccess
from nicl.euclid.pipeline import Pipeline

release_name = "Q1_R1"
esac_server_url = "https://easidr.esac.esa.int"
processing_version = "v0.7"

pipeline = partial(Pipeline,
    release_name=release_name,
    esac_server_url=esac_server_url,
    processing_version=processing_version
    )

da = DataAccess(esac_server_url=esac_server_url, release_name=release_name)
obs_ids = da.find_all_observations()
obs_ids = obs_ids[obs_ids < 4000]

with pipeline(target_obs_ids=obs_ids) as p:
    #p.create_zarr_refs(obs_ids, instrument="NIR")
    p.create_zarr_refs(obs_ids, instrument="VIS")
    p.create_coarse_data(obs_ids, instrument="NIR")
    p.create_coarse_data(obs_ids, instrument="VIS")
    p.create_nir_skyflats()
    p.create_vis_skyflats()
