"""Create cluster test images.

It is designed to be run on a supercomputer, performing the tasks for different clusters in parallel.
"""

import argparse

from nicl.euclid import testing
from nicl.euclid.utilities import default_data_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create cluster test images")
    parser.add_argument(
        "test_name",
        type=str,
        choices=["basic_test", "varying_background", "real_background"],
        help="Name of the test to create.",
    )
    parser.add_argument(
        "sky_or_cluster",
        type=str,
        choices=["sky", "cluster"],
        help="Whether to create a sky patch or a cluster image.",
    )

    args = parser.parse_args()

    testing.TEMPLATE_IMAGE_PATH = default_data_path("Q1_R1_clusters_v1.0", "TK")
    testing.TEMPLATE_IMAGE_PATH /= "EUC_NIR_W-STK_H-EDFF_eRASS_1.fits"

    if args.test_name == "basic_test":
        if args.sky_or_cluster == "sky":
            testing.create_basic_sky_test_images()
        elif args.sky_or_cluster == "cluster":
            testing.create_basic_cluster_test_images()
    elif args.test_name == "varying_background":
        if args.sky_or_cluster == "sky":
            testing.create_varying_background_sky_test_images()
        elif args.sky_or_cluster == "cluster":
            testing.create_varying_background_cluster_test_images()
    elif args.test_name == "real_background":
        if args.sky_or_cluster == "sky":
            raise ValueError(
                "Real sky patch should already exist and be linked to the test directory."
            )
        elif args.sky_or_cluster == "cluster":
            testing.create_real_background_cluster_test_images()
