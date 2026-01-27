# ensure the icl conda environment is activated, so swarp is on the path
conda activate icl

sbatch --time="7-0" stack.py EDFS I standard
sbatch stack.py EDFS Y standard
sbatch stack.py EDFS J standard
sbatch stack.py EDFS H standard
sbatch stack.py EDFS I mer
sbatch stack.py EDFS Y mer
sbatch stack.py EDFS J mer
sbatch stack.py EDFS H mer
sbatch stack.py EDFS I no_processing
sbatch stack.py EDFS Y no_processing
sbatch stack.py EDFS J no_processing
sbatch stack.py EDFS H no_processing
sbatch --time="7-0" stack.py EDFF I standard
sbatch stack.py EDFF Y standard
sbatch stack.py EDFF J standard
sbatch stack.py EDFF H standard
sbatch stack.py EDFF I mer
sbatch stack.py EDFF Y mer
sbatch stack.py EDFF J mer
sbatch stack.py EDFF H mer
sbatch stack.py EDFF I no_processing
sbatch stack.py EDFF Y no_processing
sbatch stack.py EDFF J no_processing
sbatch stack.py EDFF H no_processing
sbatch --time="7-0" stack.py EDFN I standard
sbatch stack.py EDFN Y standard
sbatch stack.py EDFN J standard
sbatch stack.py EDFN H standard
sbatch stack.py EDFN I mer
sbatch stack.py EDFN Y mer
sbatch stack.py EDFN J mer
sbatch stack.py EDFN H mer
sbatch stack.py EDFN I no_processing
sbatch stack.py EDFN Y no_processing
sbatch stack.py EDFN J no_processing
sbatch stack.py EDFN H no_processing
