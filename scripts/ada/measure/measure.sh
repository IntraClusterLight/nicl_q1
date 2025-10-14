#!/bin/bash
#SBATCH --partition=defq
#SBATCH --cpus-per-task=1
#SBATCH --mem=8g
#SBATCH --time=0:30:00
#SBATCH --output=logs/%x_%j.out

## setup conda environment
module load anaconda-uoneasy/2023.09-0
eval "$(conda shell.bash hook)"
conda activate icl

command="python ../../run_measure.py $@"
echo $command
$command
