#!/gpfs01/home/ppzsb1/.conda/envs/icl/bin/python
# fmt: off
#SBATCH --partition=defq
#SBATCH --cpus-per-task=8
#SBATCH --mem=32g
#SBATCH --time=1:00:00
#SBATCH --output=logs/%x_%j.out
# fmt: on

"""Process Q1 illustration NIR observations through the v1.0 pipeline.

The v1.0 pipeline results should be identical to the v0.7 pipeline,
as only the stacking code has been changed.

This script will perform the post-processing for observation 2683.

The command line options allow for the various corrections to be skipped,
for ablation studies.
"""

import argparse
from functools import partial

from nicl.main import configure_logging
from nicl.euclid.pipeline import Pipeline
from nicl.euclid.utilities import default_data_path

configure_logging(level="INFO")

parser = argparse.ArgumentParser(
    description="Process Q1 illustration NIR observations through the v1.0 pipeline."
)
parser.add_argument(
    "--no-skyflat",
    action="store_true",
    help="Do not apply skyflat correction.",
)
parser.add_argument(
    "--no-tartan",
    action="store_true",
    help="Do not apply skyflat correction.",
)
parser.add_argument(
    "--no-persistence",
    action="store_true",
    help="Do not apply persistence correction.",
)

args = parser.parse_args()

release_name = "Q1_R1"
esac_server_url = "https://eas.esac.esa.int"
processing_version = "v0.7"
output_path = default_data_path("Q1_R1_processed_illustration/ablation")

pipeline = partial(
    Pipeline,
    release_name=release_name,
    esac_server_url=esac_server_url,
    processing_version=processing_version,
)

obs_ids = [2683]

kwargs = dict(output_path=output_path)
if args.no_skyflat:
    kwargs.update(final_skyflat_correction=False)
if args.no_tartan:
    kwargs.update(correct_banding=False)
if args.no_persistence:
    kwargs.update(correct_persistence=False)

with pipeline(target_obs_ids=obs_ids) as p:
    p.do_persistence_correction(**kwargs)
