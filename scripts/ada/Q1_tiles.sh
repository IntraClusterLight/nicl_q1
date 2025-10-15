#!/bin/bash
#SBATCH --partition=hmemq
#SBATCH --cpus-per-task=1
#SBATCH --mem=30g
#SBATCH --time=2:00:00
#SBATCH --array=1-100%60
#SBATCH --job-name=q1_tiles
#SBATCH --output=/gpfs01/home/ppzhg/logs/Q1_tiles/%A_%a.out
#SBATCH --error=/gpfs01/home/ppzhg/logs/Q1_tiles/%A_%a.err

# Parameters:
# $1 - path to the catalog
# $2 - output directory  
# $3 - filter
# --overwrite - optional flag to overwrite existing files
# run this script with the following command:
# sbatch --mem=40g --cpus-per-task=1 --array=1-nrows%nsim Q1_tiles.sh path/to/catalog out_dir I/Y/J/H [--overwrite]

## setup conda environment
module load anaconda-uoneasy/2023.09-0
eval "$(conda shell.bash hook)"
conda activate icl

# Parse command line arguments
OVERWRITE_FLAG=""
POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    --overwrite)
      OVERWRITE_FLAG="--overwrite"
      shift # past argument
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

# Restore positional parameters
set -- "${POSITIONAL_ARGS[@]}"

# Check if we have the required positional arguments
if [ $# -lt 3 ]; then
    echo "Error: Missing required arguments"
    echo "Usage: $0 catalog_path output_dir filter [--overwrite]"
    exit 1
fi

python /gpfs01/home/ppzhg/nicl/scripts/Q1_tiles.py "$1" "$2" "$3" $SLURM_ARRAY_TASK_ID $OVERWRITE_FLAG