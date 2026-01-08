sbatch create_skypatch_mask.py EDFS VIS
sbatch create_skypatch_mask.py EDFF VIS
sbatch create_skypatch_mask.py EDFN VIS
sbatch create_skypatch_mask.py EDFS YJH
sbatch create_skypatch_mask.py EDFF YJH
sbatch create_skypatch_mask.py EDFN YJH

# The above jobs need to finish before the following jobs can be run.

sbatch measure_skypatch_noise.py EDFS VIS standard
sbatch measure_skypatch_noise.py EDFS VIS mer
sbatch measure_skypatch_noise.py EDFS VIS no_processing

sbatch measure_skypatch_noise.py EDFS Y standard
sbatch measure_skypatch_noise.py EDFS J standard
sbatch measure_skypatch_noise.py EDFS H standard
sbatch measure_skypatch_noise.py EDFS Y mer
sbatch measure_skypatch_noise.py EDFS J mer
sbatch measure_skypatch_noise.py EDFS H mer
sbatch measure_skypatch_noise.py EDFS Y no_processing
sbatch measure_skypatch_noise.py EDFS J no_processing
sbatch measure_skypatch_noise.py EDFS H no_processing

sbatch measure_skypatch_noise.py EDFF VIS standard
sbatch measure_skypatch_noise.py EDFF VIS mer
sbatch measure_skypatch_noise.py EDFF VIS no_processing

sbatch measure_skypatch_noise.py EDFF Y standard
sbatch measure_skypatch_noise.py EDFF J standard
sbatch measure_skypatch_noise.py EDFF H standard
sbatch measure_skypatch_noise.py EDFF Y mer
sbatch measure_skypatch_noise.py EDFF J mer
sbatch measure_skypatch_noise.py EDFF H mer
sbatch measure_skypatch_noise.py EDFF Y no_processing
sbatch measure_skypatch_noise.py EDFF J no_processing
sbatch measure_skypatch_noise.py EDFF H no_processing

sbatch measure_skypatch_noise.py EDFN VIS standard
sbatch measure_skypatch_noise.py EDFN VIS mer
sbatch measure_skypatch_noise.py EDFN VIS no_processing

sbatch measure_skypatch_noise.py EDFN Y standard
sbatch measure_skypatch_noise.py EDFN J standard
sbatch measure_skypatch_noise.py EDFN H standard
sbatch measure_skypatch_noise.py EDFN Y mer
sbatch measure_skypatch_noise.py EDFN J mer
sbatch measure_skypatch_noise.py EDFN H mer
sbatch measure_skypatch_noise.py EDFN Y no_processing
sbatch measure_skypatch_noise.py EDFN J no_processing
sbatch measure_skypatch_noise.py EDFN H no_processing


# The following jobs measure the noise in boxes.

sbatch measure_skypatch_noise.py EDFS VIS standard --boxes
sbatch measure_skypatch_noise.py EDFS VIS mer --boxes
sbatch measure_skypatch_noise.py EDFS VIS no_processing --boxes

sbatch measure_skypatch_noise.py EDFS Y standard --boxes
sbatch measure_skypatch_noise.py EDFS J standard --boxes
sbatch measure_skypatch_noise.py EDFS H standard --boxes
sbatch measure_skypatch_noise.py EDFS Y mer --boxes
sbatch measure_skypatch_noise.py EDFS J mer --boxes
sbatch measure_skypatch_noise.py EDFS H mer --boxes
sbatch measure_skypatch_noise.py EDFS Y no_processing --boxes
sbatch measure_skypatch_noise.py EDFS J no_processing --boxes
sbatch measure_skypatch_noise.py EDFS H no_processing --boxes

sbatch measure_skypatch_noise.py EDFF VIS standard --boxes
sbatch measure_skypatch_noise.py EDFF VIS mer --boxes
sbatch measure_skypatch_noise.py EDFF VIS no_processing --boxes

sbatch measure_skypatch_noise.py EDFF Y standard --boxes
sbatch measure_skypatch_noise.py EDFF J standard --boxes
sbatch measure_skypatch_noise.py EDFF H standard --boxes
sbatch measure_skypatch_noise.py EDFF Y mer --boxes
sbatch measure_skypatch_noise.py EDFF J mer --boxes
sbatch measure_skypatch_noise.py EDFF H mer --boxes
sbatch measure_skypatch_noise.py EDFF Y no_processing --boxes
sbatch measure_skypatch_noise.py EDFF J no_processing --boxes
sbatch measure_skypatch_noise.py EDFF H no_processing --boxes

sbatch measure_skypatch_noise.py EDFN VIS standard --boxes
sbatch measure_skypatch_noise.py EDFN VIS mer --boxes
sbatch measure_skypatch_noise.py EDFN VIS no_processing --boxes

sbatch measure_skypatch_noise.py EDFN Y standard --boxes
sbatch measure_skypatch_noise.py EDFN J standard --boxes
sbatch measure_skypatch_noise.py EDFN H standard --boxes
sbatch measure_skypatch_noise.py EDFN Y mer --boxes
sbatch measure_skypatch_noise.py EDFN J mer --boxes
sbatch measure_skypatch_noise.py EDFN H mer --boxes
sbatch measure_skypatch_noise.py EDFN Y no_processing --boxes
sbatch measure_skypatch_noise.py EDFN J no_processing --boxes
sbatch measure_skypatch_noise.py EDFN H no_processing --boxes
