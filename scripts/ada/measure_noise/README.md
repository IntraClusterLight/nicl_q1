# Scripts for creating noise profiles

## Outline

The scripts in this folder create the necessary masks then measure the noise profiles 
in the skypatch images.

## Running the processing

The commands for creating all the noise profiles are in `submit_jobs.sh`.
Note that this cannot simply be executed, one must wait for the jobs creating
the masks to complete before running the jobs to make the measurements.

### Masks

First the masks are created by the `create_skypatch_mask.py` script, e.g.
```
sbatch create_skypatch_mask.py EDFS YJH
```

### Noise measurements

After the masks have been created, the noise measurements are performed by the
`measure_skypatch_noise.py` script. This runs a task array to do the measurements
for each box size, e.g.
```
sbatch measure_skypatch_noise.py EDFS Y standard
```