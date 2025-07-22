#!/bin/bash
#SBATCH --partition=defq
#SBATCH --cpus-per-task=1
#SBATCH --mem=8g
#SBATCH --time=0:30:00

# Positional parameters:
# $1 - test name ("basic_test", "varying_background", "real_background")
# $2 - photometry filter ("Y", "J", "H", "YJH", "VIS")
# $3 - isophotes filter ("Y", "J", "H", "YJH", "VIS")
# $4 - image label ("", "no_noise")
# Run this script with the following command:
# sbatch run_measure_3_photometry.sh <test_name> <photometry_filter> <isophotes_filter> <image_label>
# All parameters variations can be safely run in parallel.
# run_measure_1_mask.sh and run_measure_2_isophotes.sh must be run first
# with the same test name and a corresponding image label.

## setup conda environment
module load anaconda-uoneasy/2023.09-0
eval "$(conda shell.bash hook)"
conda activate icl

command="python ../../run_measure.py --test-name \"$1\" --measure-photometry --photometry-filter \"$2\" --isophotes-filter \"$3\" --image-label \"$4\""
echo $command
$command