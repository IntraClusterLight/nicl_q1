#!/bin/bash
#SBATCH --partition=defq
#SBATCH --cpus-per-task=1
#SBATCH --mem=8g
#SBATCH --time=0:30:00
#SBATCH --output=logs/%x_%j.out

# Positional parameters:
# $1 - test name ("basic_test", "varying_background", "real_background")
# $2 - filter ("YJH", "VIS")
# $3 - image label ("", "no_noise")
# Run this script with the following command:
# sbatch run_measure_1_mask.sh <test_name> <filter> <image_label>
# All parameters variations can be safely run in parallel.

## setup conda environment
module load anaconda-uoneasy/2023.09-0
eval "$(conda shell.bash hook)"
conda activate icl

if [ -z "$3" ]; then
    image_label_option=""
else
    if [ "$3" == "no_noise" ]; then
        image_label_option="--image-label no_noise --true-model"
    else
        image_label_option="--image-label $3"
    fi
fi

command="python ../../run_measure.py --test-name $1 --create-masks $2 $image_label_option"
echo $command
$command