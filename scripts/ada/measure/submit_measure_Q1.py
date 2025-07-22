import subprocess

from astropy.coordinates import SkyCoord
from astropy.table import Table

if __name__ == "__main__":
    table = Table.read("~/euclid_data/catalogues/EDFS_EDFF_DES_Sample.fits")
    for row in table[:1]:
        z = str(row["BEST_Z"])
        ra = row["RA_BCG"]
        dec = row["DEC_BCG"]
        centre = SkyCoord(ra=ra, dec=dec, unit="deg")
        centre = centre.to_string()
        cluster_id = row["Label_ID"]
        cluster_id = cluster_id.replace("Cluster", "")
        initials = "TK" if cluster_id.startswith("E") else "JGM"
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
