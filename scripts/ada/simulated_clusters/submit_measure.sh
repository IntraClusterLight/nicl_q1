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
measure_mask="../../run_measure.py $args --create-masks"
measure_iso="../../run_measure.py $args --measure-isophotes --isophotes-filter"
measure_phot="../../run_measure.py $args --measure-photometry --photometry-filter"

JOB_MASK_H=$(sbatch --parsable --time=1:30:00 --job-name=mask_${label}_H $measure_mask H)
JOB_ISO_H=$(sbatch --parsable --job-name=iso_${label}_H --dependency=afterok:$JOB_MASK_H $measure_iso H --isophotes-mask-filter H)
JOB_PHOT_H_H=$(sbatch --parsable --job-name=phot_${label}_H_H --dependency=afterok:$JOB_ISO_H $measure_phot H --isophotes-filter H --isophotes-mask-filter H)
