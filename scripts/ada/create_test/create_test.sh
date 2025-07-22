#!/bin/bash
#SBATCH --partition=defq
#SBATCH --cpus-per-task=1
#SBATCH --mem=8g
#SBATCH --time=0:05:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Positional parameters:
# $1 - test name ("basic_test", "varying_background")
# $2 - cluster_or_sky ("cluster", "sky")
# Run this script with the following command:
# sbatch create_test.sh <test_name> <cluster_or_sky>
# Creating the sky requires more memory than the default:
# sbatch --mem=16g create_test.sh basic_test sky
# sbatch --mem=48g create_test.sh varying_background sky 
# All parameters variations can be safely run in parallel, as can cluster and sky scripts.

## setup conda environment
module load anaconda-uoneasy/2023.09-0
eval "$(conda shell.bash hook)"
conda activate icl

command="python ../../run_create_test.py $1 $2"
echo $command
$command