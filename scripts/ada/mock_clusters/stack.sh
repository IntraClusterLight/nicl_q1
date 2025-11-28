#!/bin/bash
#SBATCH --partition=defq
#SBATCH --cpus-per-task=1
#SBATCH --mem=16g
#SBATCH --time=0:20:00
#SBATCH --array=1-4
#SBATCH --job-name=mock_clusters_stack
#SBATCH --output=logs/%x_%A_%a.out

# Positional parameters:
# $1 - filter
# $2 - variant
# run this script with the following command:
# sbatch stack.sh I/Y/J/H

## setup conda environment
module load anaconda-uoneasy/2023.09-0
eval "$(conda shell.bash hook)"
conda activate icl

if [ -n "$2" ]; then
    variant="--variant $2"
else
    variant=""
fi

python stack.py mock_clusters.txt  ~/euclid_data/Q1_R1_mock_clusters_v1.0/ $1 $variant $SLURM_ARRAY_TASK_ID