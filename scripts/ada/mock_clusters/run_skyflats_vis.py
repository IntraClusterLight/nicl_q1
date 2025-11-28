#!/gpfs01/home/ppzsb1/.conda/envs/icl/bin/python
# fmt: off
#SBATCH --partition=defq
#SBATCH --cpus-per-task=8
#SBATCH --mem=32g
#SBATCH --time=3:00:00
#SBATCH --output=logs/%x_%j.out
# fmt: on

"""Create VIS skyflats for Q1 Mock Cluster NIR observations.

The data in Q1_R1_mock_clusters is symlinked to the Q1_R1 data,
except for observation 3591, which has had nine mock clusters injected.

To save time, the zarr folder has already been created in Q1_R1_mock_clusters,
with symlinks to the Q1_R1_processed_v0.7/zarr folder, except for observation 3591.

This script will create the skyflats for observation 3591.
"""

from functools import partial

from nicl.main import configure_logging
from nicl.euclid.pipeline import Pipeline

configure_logging(level="INFO")
configure_logging(name="nicl.mask", level="WARNING")

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

obs_ids = [3582, 3583, 3590, 3591, 3592, 3593, 3594]

with pipeline(target_obs_ids=obs_ids) as p:
    p.create_vis_skyflats()
