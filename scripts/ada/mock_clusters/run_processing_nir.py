#!/gpfs01/home/ppzsb1/.conda/envs/icl/bin/python
# fmt: off
#SBATCH --partition=defq
#SBATCH --cpus-per-task=8
#SBATCH --mem=32g
#SBATCH --time=1:00:00
#SBATCH --output=logs/%x_%j.out
# fmt: on

"""Process Q1 Mock Cluster NIR observations through the v1.0 pipeline.

The v1.0 pipeline results should be identical to the v0.7 pipeline,
as only the stacking code has been changed.

The data in Q1_R1_mock_clusters is symlinked to the Q1_R1 data,
except for observation 3591, which has had nine mock clusters injected.

To save time, the zarr folder has already been created in Q1_R1_mock_clusters,
with symlinks to the Q1_R1_processed_v0.7/zarr folder, except for observation 3591.

The skyflat for 3591 must first be created using the run_skyflats_nir.py script.

This script will perform the post-processing for observation 3591.

The command line options allow for the various corrections to be skipped,
for ablation studies.
"""

import argparse
from functools import partial

from nicl.main import configure_logging
from nicl.euclid.pipeline import Pipeline

configure_logging(level="INFO")

parser = argparse.ArgumentParser(
    description="Process Q1 Mock Cluster NIR observations through the v1.0 pipeline."
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
release_folder_name = "Q1_R1_mock_clusters"
esac_server_url = "https://eas.esac.esa.int"
processing_version = "v1.0"

pipeline = partial(
    Pipeline,
    release_name=release_name,
    release_folder_name=release_folder_name,
    esac_server_url=esac_server_url,
    processing_version=processing_version,
)

obs_ids = [3591]

kwargs = {}
if args.no_skyflat:
    kwargs.update(final_skyflat_correction=False)
if args.no_tartan:
    kwargs.update(correct_banding=False)
if args.no_persistence:
    kwargs.update(correct_persistence=False)

with pipeline(target_obs_ids=obs_ids) as p:
    p.do_persistence_correction(**kwargs)
