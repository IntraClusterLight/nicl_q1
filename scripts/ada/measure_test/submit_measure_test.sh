#! /bin/bash

# Submit all jobs for a test in parallel
# Positional parameters:
# $1 - test name ("basic_test", "varying_background", "real_background")
# $2 - image label ("", "no_noise")
# Run this script with the following command:
# submit_measure_test.sh <test_name> <image_label>

JOB_MASK_YJH=$(sbatch measure_test_1_mask.sh $1 YJH $2)

JOB_ISO_YJH=$(sbatch --dependency=afterok:$JOB_MASK_YJH measure_test_2_isophotes.sh $1 YJH $2)
JOB_PHOT_YJH=$(sbatch --dependency=afterok:$JOB_ISO_YJH measure_test_3_photometry.sh $1 YJH $2)

JOB_ISO_Y=$(sbatch --dependency=afterok:$JOB_MASK_YJH measure_test_2_isophotes.sh $1 Y $2)
JOB_PHOT_Y_Y=$(sbatch --dependency=afterok:$JOB_ISO_Y measure_test_3_photometry.sh $1 Y Y $2)
JOB_PHOT_Y_YJH=$(sbatch --dependency=afterok:$JOB_ISO_Y measure_test_3_photometry.sh $1 Y YJH $2)

JOB_ISO_J=$(sbatch --dependency=afterok:$JOB_MASK_YJH measure_test_2_isophotes.sh $1 J $2)
JOB_PHOT_J_J=$(sbatch --dependency=afterok:$JOB_ISO_J measure_test_3_photometry.sh $1 J J $2)
JOB_PHOT_J_YJH=$(sbatch --dependency=afterok:$JOB_ISO_J measure_test_3_photometry.sh $1 J YJH $2)

JOB_ISO_H=$(sbatch --dependency=afterok:$JOB_MASK_YJH measure_test_2_isophotes.sh $1 H $2)
JOB_PHOT_H_H=$(sbatch --dependency=afterok:$JOB_ISO_H measure_test_3_photometry.sh $1 H H $2)
JOB_PHOT_H_YJH=$(sbatch --dependency=afterok:$JOB_ISO_H measure_test_3_photometry.sh $1 H YJH $2)


JOB_MASK_VIS=$(sbatch measure_test_1_mask.sh $1 VIS $2)

JOB_ISO_VIS=$(sbatch --dependency=afterok:$JOB_MASK_VIS measure_test_2_isophotes.sh $1 VIS $2)
JOB_PHOT_VIS_VIS=$(sbatch --dependency=afterok:$JOB_ISO_VIS measure_test_3_photometry.sh $1 VIS VIS $2)
JOB_PHOT_VIS_YJH=$(sbatch --dependency=afterok:$JOB_ISO_VIS measure_test_3_photometry.sh $1 VIS YJH $2)