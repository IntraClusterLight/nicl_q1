"""Process Q1 observations through the v0.7 pipeline.

The changes since v0.6 are:
- The skyflat/autodarks have the median level restored
- Use the new pipeline class to process the data
"""

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
obs_ids = obs_ids[obs_ids % 10 == 0]


with pipeline(target_obs_ids=obs_ids) as p:
    p.create_vis_skyflats()
    p.create_nir_skyflats()
    p.do_persistence_correction()
    for bkg_sub in [False, True]:
        p.create_stacks(bkg_sub=bkg_sub)
        p.calculate_background_stats(bkg_sub=bkg_sub)
