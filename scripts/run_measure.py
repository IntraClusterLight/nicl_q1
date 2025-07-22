"""Run all the tasks for measuring the surface brightness profile of a cluster.

It is designed to be run on a supercomputer, performing the tasks for different filters and clusters in parallel.

The masks must be created first, and then the isophotes and photometry can be measured.
"""

import argparse
import logging

from nicl import configure_logging
from nicl.euclid.measure import ClusterPipeline
from nicl.euclid.utilities import default_data_path

if __name__ == "__main__":
    configure_logging(logfile=default_data_path("test_measure") / "measure.log")
    configure_logging(name="__main__", level="DEBUG")
    configure_logging(name="nicl.euclid.mask", level="DEBUG")
    configure_logging(name="nicl.mask", level="DEBUG")
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(
        description="Run ICL measurements on a cluster image."
    )
    parser.add_argument(
        "--test-name",
        type=str,
        help="If a test is being run, specify the name of the test.",
    )
    parser.add_argument(
        "--cluster-id",
        type=str,
        help="ID of the cluster.",
    )
    parser.add_argument(
        "--cluster-z",
        type=float,
        help="Redshift of the cluster.",
    )
    parser.add_argument(
        "--cluster-centre",
        type=str,
        help="RA and Dec of the centre of the cluster.",
    )
    parser.add_argument(
        "--image-dir",
        type=str,
        help="Name of the directory containing the images.",
    )
    parser.add_argument(
        "--image-label",
        type=str,
        help="Label of the image to process.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Name of the directory in which to save the output.",
        required=True,
    )
    parser.add_argument(
        "--isophotes-filter",
        type=str,
        choices=["Y", "J", "H", "YJH", "VIS"],
        help="Filter in which to measure isophotes.",
    )
    parser.add_argument(
        "--photometry-filter",
        type=str,
        choices=["Y", "J", "H", "YJH", "VIS"],
        help="Filter in which to measure photometry.",
    )
    process = parser.add_mutually_exclusive_group(required=True)
    process.add_argument(
        "--create-masks",
        type=str,
        choices=["YJH", "VIS"],
        help="Create masks in the specified filter.",
    )
    process.add_argument(
        "--measure-isophotes",
        action="store_true",
        help="Measure isophotes.",
    )
    process.add_argument(
        "--measure-photometry",
        action="store_true",
        help="Measure photometry.",
    )

    args = parser.parse_args()
    if args.test_name:
        args.cluster_id = "cluster"
        args.cluster_z = 0.1
        args.cluster_centre = None
        args.image_dir = f"test_images/{args.test_name}"
        args.output_dir = f"test_measure/{args.test_name}"
    image_path = default_data_path(args.image_dir) / args.name
    out_path = default_data_path(args.output_dir) / args.name
    if args.create_masks:
        mask_filter = args.create_masks
    else:
        if args.measure_isophotes:
            filter = args.isophotes_filter
        elif args.measure_photometry:
            filter = args.photometry_filter
        mask_filter = "VIS" if filter == "VIS" else "YJH"

    pipeline = ClusterPipeline(
        image_dir=image_path,
        image_label=args.image_label,
        output_dir=out_path,
        cluster_id=args.cluster_id,
        cluster_z=args.cluster_z,
        bcg_pos=args.cluster_centre,
        filters=args.photometry_filter,
        mask_filter=mask_filter,
        isophotes_filter=args.isophotes_filter,
    )
    if args.create_masks:
        logger.info(f"Creating masks for {args.cluster_id} in filter {mask_filter}")
        logger.info(f"Cluster redshift: {args.cluster_z}")
        if args.cluster_centre:
            logger.info(f"Cluster centre: {args.cluster_centre}")
        else:
            logger.info("Assuming cluster is at the centre of the image")
        logger.info(f"Using images from {image_path}")
        if args.image_label:
            logger.info(f"With image label {args.image_label}")
        logger.info(f"Saving masks to {out_path}")
        pipeline.create_masks()
    elif args.measure_isophotes:
        logger.info(
            f"Measuring isophotes for {args.cluster_id} in filter {args.isophotes_filter}"
        )
        logger.info(f"Cluster redshift: {args.cluster_z}")
        if args.cluster_centre:
            logger.info(f"Cluster centre: {args.cluster_centre}")
        else:
            logger.info("Assuming cluster is at the centre of the image")
        logger.info(f"Using images from {image_path}")
        if args.image_label:
            logger.info(f"With image label {args.image_label}")
        logger.info(f"Saving isophotes to {out_path}")
        pipeline.measure_isophotes(args.isophotes_filter)
    elif args.measure_photometry:
        pipeline.measure_photometry(
            args.photometry_filter, isophotes_filter=args.isophotes_filter
        )
