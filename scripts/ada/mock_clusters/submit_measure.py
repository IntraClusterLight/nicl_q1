import argparse
import subprocess

from astropy.coordinates import SkyCoord
from astropy.table import Table

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure Q1 mock clusters")
    parser.add_argument(
        "--variant",
        type=str,
        choices=[
            "standard",
            "no_processing",
            "no_skyflat",
            "no_bkg_match",
            "no_persistence",
            "no_tartan",
        ],
        default="standard",
        help="Variant of the data processing to be measured.",
    )
    args = parser.parse_args()
    variant = args.variant

    table = Table.read("mock_clusters.txt", format="ascii")
    z = "0.1"
    for row in table:
        ra = row[1]
        dec = row[2]
        centre = SkyCoord(ra=ra, dec=dec, unit="deg")
        centre = centre.to_string(precision=8)
        cluster_id = row[0]
        image_dir = f"Q1_R1_mock_clusters_v1.0/{variant}"
        output_dir = f"Q1_R1_mock_clusters_v1.0_measurements/{variant}"
        label = f"{cluster_id}"
        process_vis = "False" if variant in ["no_persistence", "no_tartan"] else "True"
        args = ["./submit_measure.sh", label, process_vis]
        args += ["--image-dir", image_dir]
        args += ["--output-dir", output_dir]
        args += ["--cluster-id", cluster_id]
        args += ["--cluster-z", z]
        args += ["--cluster-centre", centre]
        subprocess.run(args)
