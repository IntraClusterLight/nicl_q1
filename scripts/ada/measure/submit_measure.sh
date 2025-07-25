#! /bin/bash

# Submit all jobs for a test in parallel
# Positional parameters:
# $1 - label (for job name)
# $2, etc. - arguments to measure.sh
# Run this script with the following command:
# submit_measure.sh <label> <args>

if [ -z "$1" ]; then
    echo "Error: Arguments are required"
    exit 1
fi

label=$1; shift
args="$@"
measure_mask="measure.sh $args --create-masks"
measure_iso="measure.sh $args --measure-isophotes --isophotes-filter"
measure_phot="measure.sh $args --measure-photometry --photometry-filter"

JOB_MASK_YJH=$(sbatch --parsable --time=1:00:00 --job-name=mask_${label}_YJH $measure_mask YJH)

JOB_ISO_YJH=$(sbatch --parsable --job-name=iso_${label}_YJH --dependency=afterok:$JOB_MASK_YJH $measure_iso YJH)
JOB_PHOT_YJH_YJH=$(sbatch --parsable --job-name=phot_${label}_YJH_YJH --dependency=afterok:$JOB_ISO_YJH $measure_phot YJH --isophotes-filter YJH)

JOB_ISO_Y=$(sbatch --parsable --job-name=iso_${label}_Y --dependency=afterok:$JOB_MASK_YJH $measure_iso Y)
JOB_PHOT_Y_Y=$(sbatch --parsable --job-name=phot_${label}_Y_Y --dependency=afterok:$JOB_ISO_Y $measure_phot Y --isophotes-filter Y)
JOB_PHOT_Y_YJH=$(sbatch --parsable --job-name=phot_${label}_Y_YJH --dependency=afterok:$JOB_ISO_Y:$JOB_PHOT_Y_Y $measure_phot Y --isophotes-filter YJH)

JOB_ISO_J=$(sbatch --parsable --job-name=iso_${label}_J --dependency=afterok:$JOB_MASK_YJH $measure_iso J)
JOB_PHOT_J_J=$(sbatch --parsable --job-name=phot_${label}_J_J --dependency=afterok:$JOB_ISO_J $measure_phot J --isophotes-filter J)
JOB_PHOT_J_YJH=$(sbatch --parsable --job-name=phot_${label}_J_YJH --dependency=afterok:$JOB_ISO_J:$JOB_PHOT_J_J $measure_phot J --isophotes-filter YJH)

JOB_ISO_H=$(sbatch --parsable --job-name=iso_${label}_H --dependency=afterok:$JOB_MASK_YJH $measure_iso H)
JOB_PHOT_H_H=$(sbatch --parsable --job-name=phot_${label}_H_H --dependency=afterok:$JOB_ISO_H $measure_phot H --isophotes-filter H)
JOB_PHOT_H_YJH=$(sbatch --parsable --job-name=phot_${label}_H_YJH --dependency=afterok:$JOB_ISO_H:$JOB_PHOT_H_H $measure_phot H --isophotes-filter YJH)


JOB_MASK_VIS=$(sbatch --parsable --job-name=mask_${label}_VIS $measure_mask VIS)

JOB_ISO_VIS=$(sbatch --parsable --job-name=iso_${label}_VIS --dependency=afterok:$JOB_MASK_VIS $measure_iso VIS)
JOB_PHOT_VIS_VIS=$(sbatch --parsable --job-name=phot_${label}_VIS_VIS --dependency=afterok:$JOB_ISO_VIS $measure_phot VIS --isophotes-filter VIS)
JOB_PHOT_VIS_YJH=$(sbatch --parsable --job-name=phot_${label}_VIS_YJH --dependency=afterok:$JOB_ISO_VIS:$JOB_PHOT_VIS_VIS $measure_phot VIS --isophotes-filter YJH)