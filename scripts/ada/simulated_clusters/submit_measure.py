import subprocess

from astropy.coordinates import SkyCoord
from astropy.table import Table

from nicl.euclid.utilities import default_data_path

if __name__ == "__main__":
    table = Table.read(
        default_data_path("catalogues/Hydrangea_Mocks_Sample.csv"), format="csv"
    )
    for row in table[:1]:
        for subfolder in ["with_subhaloes", "without_subhaloes"]:
            image_dir = f"Q1_R1_simulated_clusters/{subfolder}/images"
            output_dir = f"Q1_R1_simulated_clusters/{subfolder}/measurements/"
            ra = row["RA"]
            dec = row["Dec"]
            centre = SkyCoord(ra=ra, dec=dec, unit="deg")
            centre = centre.to_string(precision=8)
            cluster_id = row["ID"]
            z = str(row["Redshift"])
            label = f"{cluster_id}"
            args = ["./submit_measure.sh", label]
            args += ["--image-dir", image_dir]
            args += ["--output-dir", output_dir]
            args += ["--cluster-id", cluster_id]
            args += ["--cluster-z", z]
            args += ["--cluster-centre", centre]
            subprocess.run(args)
