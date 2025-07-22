#!/bin/bash
#SBATCH --partition=defq
#SBATCH --cpus-per-task=1
#SBATCH --mem=8g
#SBATCH --time=0:30:00
#SBATCH --output=logs/%x_%j.out

# Positional parameters:
# $1 - test name ("basic_test", "varying_background", "real_background")
# $2 - filter ("YJH", "VIS")
# Run this script with the following command:
# sbatch run_measure_1_mask.sh <test_name> <filter>
# All parameters variations can be safely run in parallel.

## setup conda environment
module load anaconda-uoneasy/2023.09-0
eval "$(conda shell.bash hook)"
conda activate icl

command="python ../../run_measure.py --test-name $1 --create-masks $2"
echo $command
$command