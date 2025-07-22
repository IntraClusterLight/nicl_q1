#! /bin/bash

# Submit all jobs to create all test images in parallel
# Run this script with the following command:
# submit_create_test.sh

sbatch --mem=16g create_test.sh basic_test sky
sbatch create_test.sh basic_test cluster
sbatch --mem=48g create_test.sh varying_background sky
sbatch create_test.sh varying_background cluster
SKY_PATCH_DIR=~/euclid_data/Q1_R1_clusters_v1.0/skypatch
TEST_IMAGES_DIR=~/euclid_data/test_images
REAL_BACKGROUND_DIR=${TEST_IMAGES_DIR}/real_background
ln -s $SKY_PATCH_DIR/EUC_NIR_W-STK_H-EDFS_sky.fits $REAL_BACKGROUND_DIR/EUC_NIR_W-STK_H-sky_patch.fits
ln -s $SKY_PATCH_DIR/EUC_NIR_W-STK_J-EDFS_sky.fits $REAL_BACKGROUND_DIR/EUC_NIR_W-STK_J-sky_patch.fits
ln -s $SKY_PATCH_DIR/EUC_NIR_W-STK_Y-EDFS_sky.fits $REAL_BACKGROUND_DIR/EUC_NIR_W-STK_Y-sky_patch.fits
ln -s $SKY_PATCH_DIR/EUC_VIS_SWL-STK-EDFS_sky.fits $REAL_BACKGROUND_DIR/EUC_VIS_SWL-STK-sky_patch.fits
sbatch create_test.sh real_background cluster
chmod -R a+rX $TEST_IMAGES_DIR