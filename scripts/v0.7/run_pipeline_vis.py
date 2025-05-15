"""Process Q1 VIS observations through the v0.7 pipeline.

The changes since v0.6 are:
- The skyflat/autodarks have the median level restored
- Improvements to masking for skyflats
- Use the new pipeline class to process the data
"""

from functools import partial

from nicl.euclid.data_access import DataAccess
from nicl.euclid.pipeline import Pipeline


release_name = "Q1_R1"
esac_server_url = "https://easidr.esac.esa.int"
processing_version = "v0.7"

pipeline = partial(
    Pipeline,
    release_name=release_name,
    esac_server_url=esac_server_url,
    processing_version=processing_version,
)

da = DataAccess(esac_server_url=esac_server_url, release_name=release_name)
obs_ids = da.find_all_observations()
obs_ids = obs_ids[obs_ids < 4000]

with pipeline(target_obs_ids=obs_ids) as p:
    p.get_vis_data()
    p.create_vis_skyflats()
    p.create_stacks(instrument="VIS", bkg_sub=False)
    p.calculate_background_stats(instrument="VIS", bkg_sub=False)
