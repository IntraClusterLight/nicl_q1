#!/bin/bash
#SBATCH --partition=defq
#SBATCH --cpus-per-task=1
#SBATCH --mem=16g
#SBATCH --time=2:00:00
#SBATCH --array=0-31
## #SBATCH --array=1:127%32

## setup environment
module load anaconda-uoneasy/2023.09-0

export PATH=/gpfs01/home/ppzsb1/.conda/envs/icl/bin:$PATH

which python

files=(~/euclid_data/Q1_R1/NIR/*)
if [ "${SLURM_ARRAY_TASK_ID}" -lt "${#files[@]}" ]; then
    obs_id="${files[$SLURM_ARRAY_TASK_ID]##*/}"
    python do_persistence_correction.py $obs_id
fi
