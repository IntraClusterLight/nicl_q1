sbatch --time=0:30:00 stack.sh I
sbatch stack.sh Y
sbatch stack.sh J
sbatch stack.sh H
sbatch --mem=64g --time=2:00:00 stack.sh I no_processing
sbatch stack.sh Y no_processing
sbatch stack.sh J no_processing
sbatch stack.sh H no_processing
sbatch stack.sh I no_bkg_match
sbatch stack.sh Y no_bkg_match
sbatch stack.sh J no_bkg_match
sbatch stack.sh H no_bkg_match
sbatch --mem=64g --time=2:00:00 stack.sh I no_skyflat
sbatch stack.sh Y no_skyflat
sbatch stack.sh J no_skyflat
sbatch stack.sh H no_skyflat
sbatch stack.sh Y no_tartan
sbatch stack.sh J no_tartan
sbatch stack.sh H no_tartan
sbatch stack.sh Y no_persistence
sbatch stack.sh J no_persistence
sbatch stack.sh H no_persistence
