#!/bin/bash
#SBATCH --partition=defq
#SBATCH --cpus-per-task=8
#SBATCH --mem=64g
#SBATCH --time=4:00:00

## setup environment
module load anaconda-uoneasy/2023.09-0

export PATH=/gpfs01/home/ppzsb1/.conda/envs/icl/bin:$PATH

python run_pipeline_nir.py
