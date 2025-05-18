#!/bin/bash
#SBATCH --partition=defq
#SBATCH --cpus-per-task=1
#SBATCH --mem=30g
#SBATCH --time=2:00:00
#SBATCH --array=1-100%60
#SBATCH --job-name=q1_stack
#SBATCH --output=/gpfs01/home/ppzhg/logs/Q1_stack/%A_%a.out
#SBATCH --error=/gpfs01/home/ppzhg/logs/Q1_stack/%A_%a.err

# Positional parameters:
# $1 - path to the catalog
# $2 - output subfolder
# $3 - instrument (VIS or NISP)
# run this script with the following command:
# sbatch --mem=40g --cpus-per-task=3 --array=1-nrows stack_Q1.sh path/to/catalog subfolder VIS|NISP

## setup conda environment
module load anaconda-uoneasy/2023.09-0
eval "$(conda shell.bash hook)"
conda activate icl

python /gpfs01/home/ppzhg/nicl/scripts/stack_Q1.py "$1" "$2" "$3" $SLURM_ARRAY_TASK_ID