#! /bin/bash

# Submit all jobs for a test in parallel
# Positional parameters:
# $1 - test name ("basic_test", "varying_background", "real_background")
# $2 - image label ("", "no_noise")
# Run this script with the following command:
# submit_measure_test.sh <test_name> <image_label>

if [ -z "$2" ]; then
    label=$1
else
    label=${1}_${2}
fi

JOB_MASK_YJH=$(sbatch --parsable --job-name=mask_${label}_YJH measure_test_1_mask.sh $1 YJH $2)

JOB_ISO_YJH=$(sbatch --parsable --job-name=iso_${label}_YJH --dependency=afterok:$JOB_MASK_YJH measure_test_2_isophotes.sh $1 YJH $2)
JOB_PHOT_YJH_YJH=$(sbatch --parsable --job-name=phot_${label}_YJH_YJH --dependency=afterok:$JOB_ISO_YJH measure_test_3_photometry.sh $1 YJH YJH $2)

JOB_ISO_Y=$(sbatch --parsable --job-name=iso_${label}_Y --dependency=afterok:$JOB_MASK_YJH measure_test_2_isophotes.sh $1 Y $2)
JOB_PHOT_Y_Y=$(sbatch --parsable --job-name=phot_${label}_Y_Y --dependency=afterok:$JOB_ISO_Y measure_test_3_photometry.sh $1 Y Y $2)
JOB_PHOT_Y_YJH=$(sbatch --parsable --job-name=phot_${label}_Y_YJH --dependency=afterok:$JOB_ISO_YJH measure_test_3_photometry.sh $1 Y YJH $2)

JOB_ISO_J=$(sbatch --parsable --job-name=iso_${label}_J --dependency=afterok:$JOB_MASK_YJH measure_test_2_isophotes.sh $1 J $2)
JOB_PHOT_J_J=$(sbatch --parsable --job-name=phot_${label}_J_J --dependency=afterok:$JOB_ISO_J measure_test_3_photometry.sh $1 J J $2)
JOB_PHOT_J_YJH=$(sbatch --parsable --job-name=phot_${label}_J_YJH --dependency=afterok:$JOB_ISO_YJH measure_test_3_photometry.sh $1 J YJH $2)

JOB_ISO_H=$(sbatch --parsable --job-name=iso_${label}_H --dependency=afterok:$JOB_MASK_YJH measure_test_2_isophotes.sh $1 H $2)
JOB_PHOT_H_H=$(sbatch --parsable --job-name=phot_${label}_H_H --dependency=afterok:$JOB_ISO_H measure_test_3_photometry.sh $1 H H $2)
JOB_PHOT_H_YJH=$(sbatch --parsable --job-name=phot_${label}_H_YJH --dependency=afterok:$JOB_ISO_YJH measure_test_3_photometry.sh $1 H YJH $2)


JOB_MASK_VIS=$(sbatch --parsable --job-name=mask_${label}_VIS measure_test_1_mask.sh $1 VIS $2)

JOB_ISO_VIS=$(sbatch --parsable --job-name=iso_${label}_VIS --dependency=afterok:$JOB_MASK_VIS measure_test_2_isophotes.sh $1 VIS $2)
JOB_PHOT_VIS_VIS=$(sbatch --parsable --job-name=phot_${label}_VIS_VIS --dependency=afterok:$JOB_ISO_VIS measure_test_3_photometry.sh $1 VIS VIS $2)
JOB_PHOT_VIS_YJH=$(sbatch --parsable --job-name=phot_${label}_VIS_YJH --dependency=afterok:$JOB_MASK_VIS:$JOB_ISO_YJH measure_test_3_photometry.sh $1 VIS YJH $2)