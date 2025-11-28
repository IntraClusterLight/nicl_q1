#!/gpfs01/home/ppzsb1/.conda/envs/icl/bin/python
# fmt: off
#SBATCH --partition=defq
#SBATCH --cpus-per-task=8
#SBATCH --mem=16g
#SBATCH --time=0:15:00
#SBATCH --output=logs/%x_%j.out
# fmt: on

"""Process Q1 illustration persistence debug corrections with the v1.0 pipeline.

The v1.0 pipeline results should be identical to the v0.7 pipeline,
as only the stacking code has been changed.

This script will perform the post-processing for observation 2683, detector 11
with debug output.
"""

from functools import partial

from nicl.main import configure_logging
from nicl.euclid.pipeline import Pipeline
from nicl.euclid.utilities import default_data_path

configure_logging(level="INFO")

release_name = "Q1_R1"
esac_server_url = "https://eas.esac.esa.int"
processing_version = "v0.7"
output_path = default_data_path("Q1_R1_processed_illustration")

pipeline = partial(
    Pipeline,
    release_name=release_name,
    esac_server_url=esac_server_url,
    processing_version=processing_version,
)

obs_ids = [2683]
kwargs = dict(output_path=output_path, detector=11, debug=True)

with pipeline(target_obs_ids=obs_ids) as p:
    p.do_persistence_correction(**kwargs)
