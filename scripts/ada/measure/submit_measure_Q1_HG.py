import subprocess

from astropy.coordinates import SkyCoord
from astropy.table import Table

todo = [
    "EUC-CLJ0335-2928",
    "EUC-CLJ0401-4933",
    "EUC-CLJ0413-4807",
    "EUC-CLJ0420-4615",
    "EUC-CLJ0423-4650",
    "EUC-CLJ0424-4701",
    "EUC-CLJ0424-4706",
    "EUC-CLJ0424-4800",
    "EUC-CLJ0424-4806",
    "EUC-CLJ1743+6410",
    "EUC-CLJ1750+6524",
    "EUC-CLJ1803+6357",
    "EUC-CLJ1803+6400",
    "EUC-CLJ1806+6356",
    "EUC-CLJ1811+6443",
    "EUC-CLJ1821+6642",
    "EUC-CLJ1822+6536",
    "EUC-CLJ1822+6648",
    "SPT-CLJ0344-4933",
    "SPT-CLJ0353-5043",
]

if __name__ == "__main__":
    table = Table.read("~/euclid_data/catalogues/Clusters_HG.fits")
    for row in table:
        z = str(row["z"])
        if z == "--":
            continue
        ra = row["BCG RA"]
        dec = row["BCG Dec"]
        centre = SkyCoord(ra=ra, dec=dec, unit="deg")
        centre = centre.to_string(precision=8)
        cluster_id = row["Cluster"]
        if cluster_id not in todo:
            continue
        initials = "HG"
        image_dir = f"Q1_R1_clusters_v1.0/{initials}"
        output_dir = f"measurements/{initials}"
        label = f"{initials}_{cluster_id}"
        args = ["./submit_measure.sh", label]
        args += ["--image-dir", image_dir]
        args += ["--output-dir", output_dir]
        args += ["--cluster-id", cluster_id]
        args += ["--cluster-z", z]
        args += ["--cluster-centre", centre]
        subprocess.run(args)
