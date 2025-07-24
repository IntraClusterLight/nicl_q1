"""Run all the tasks for measuring the surface brightness profile of a cluster.

It is designed to be run on a supercomputer, performing the tasks for different filters and clusters in parallel.

The masks must be created first, and then the isophotes and photometry can be measured.
"""

import argparse
import logging

from astropy.coordinates import SkyCoord

from nicl import configure_logging
from nicl.euclid.measure import ClusterPipeline
from nicl.euclid.utilities import default_data_path

if __name__ == "__main__":
    configure_logging(level="DEBUG")
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
        nargs=2,
        type=float,
        help="RA and Dec of the centre of the cluster, in degrees",
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
    parser.add_argument(
        "--true-model",
        action="store_true",
        help="Measuring a true model, i.e. do not use a mask, do not estimate background.",
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
    else:
        if None in [args.cluster_id, args.cluster_z, args.image_dir, args.output_dir]:
            parser.error("Missing required arguments")
    image_path = default_data_path(args.image_dir)
    out_path = default_data_path(args.output_dir)
    box_size = None  # use the default box size of 1 Mpc
    if args.cluster_centre:
        cluster_centre = SkyCoord(
            ra=args.cluster_centre[0], dec=args.cluster_centre[1], unit="deg"
        )
    else:
        cluster_centre = None
    if args.create_masks:
        mask_filter = args.create_masks
        filters = mask_filter
    else:
        if args.measure_isophotes:
            filters = args.isophotes_filter
        elif args.measure_photometry:
            filters = args.photometry_filter
        if args.true_model:
            mask_filter = None
            box_size = False  # do not subtract a background
        else:
            mask_filter = "VIS" if filters == "VIS" else "YJH"

    # We only allow use of matching labels. In principle, this could be relaxed, to
    # allow photometry on the noisy images using isophotes from the true model.
    mask_label = isophotes_label = args.image_label

    pipeline = ClusterPipeline(
        image_dir=image_path,
        image_label=args.image_label,
        output_dir=out_path,
        cluster_id=args.cluster_id,
        cluster_z=args.cluster_z,
        box_size=box_size,
        bcg_pos=cluster_centre,
        filters=filters,
        mask_filter=mask_filter,
        isophotes_filter=args.isophotes_filter,
        mask_label=mask_label,
        isophotes_label=isophotes_label,
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
