#!/gpfs01/home/ppzsb1/.conda/envs/icl/bin/python
# fmt: off
#SBATCH --partition=defq
#SBATCH --cpus-per-task=1
#SBATCH --mem=8g
#SBATCH --time=1:00:00
#SBATCH --array=1-819
#SBATCH --output=logs/%x_%j.out
# fmt: on

import os

from astropy.coordinates import SkyCoord
from astropy.table import Table

from nicl import configure_logging
from nicl.euclid.measure import ClusterPipeline
from nicl.euclid.utilities import default_data_path

if __name__ == "__main__":
    configure_logging(level="DEBUG")
    configure_logging(name="nicl.mask", level="INFO")
    data_path = default_data_path("Q1_R1_simulated_clusters")
    table = Table.read(
        default_data_path("catalogues/Hydrangea_Mocks_Sample.csv"), format="csv"
    )
    # There are 819 rows in this table
    task_id = int(os.getenv("SLURM_ARRAY_TASK_ID"))
    row = table[task_id - 1]
    for subfolder in ["with_subhaloes", "without_subhaloes"]:
        image_dir = data_path / f"{subfolder}/images"
        output_dir = data_path / f"{subfolder}/measurements/"
        ra = row["RA"]
        dec = row["Dec"]
        centre = SkyCoord(ra=ra, dec=dec, unit="deg")
        cluster_id = row["ID"]
        z = float(row["Redshift"])
        filter = row["band"]
        pipeline = ClusterPipeline(
            image_dir=image_dir,
            output_dir=output_dir,
            cluster_id=cluster_id,
            cluster_z=z,
            bcg_pos=centre,
            filters=filter,
            mask_filter=filter,
            isophotes_filter=filter,
        )
        pipeline.run()
