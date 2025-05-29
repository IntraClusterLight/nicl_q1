"""Process a set of OTF observations through the pipeline for cirrus project."""

from functools import partial

from nicl.euclid.pipeline import Pipeline


release_name = "OTF"
esac_server_url = "https://easotf.esac.esa.int"
processing_version = "v0.7"

pipeline = partial(
    Pipeline,
    release_name=release_name,
    esac_server_url=esac_server_url,
    processing_version=processing_version,
)

obs_ids = [
    801,
    800,
    739,
    336,
    822,
    707,
    502,
    305,
    979,
    412,
    178,
    141,
    326,
    335,
    412,
    491,
    57,
    625,
    706,
    712,
    739,
    770,
    783,
    801,
    822,
    871,
    321,
    333,
    336,
    471,
    502,
    618,
    697,
    738,
    765,
    780,
    800,
    819,
    856,
    979,
]
obs_ids = sorted(list(set(obs_ids)))

with pipeline(target_obs_ids=obs_ids, max_workers=4) as p:
    p.get_vis_data()
    p.create_vis_skyflats()
    p.create_stacks(instrument="VIS", bkg_sub=False)
    p.calculate_background_stats(instrument="VIS", bkg_sub=False)
