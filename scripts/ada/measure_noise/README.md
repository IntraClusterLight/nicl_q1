# Scripts for creating noise profiles

## Outline

The scripts in this folder create the necessary masks then measure the noise profiles 
in the skypatch images.

## Running the processing

### Masks

First the masks are created by the `create_skypatch_mask.py` script.
```
sbatch create_skypatch_mask.py EDFS YJH
sbatch create_skypatch_mask.py EDFS VIS
sbatch create_skypatch_mask.py EDFF YJH
sbatch create_skypatch_mask.py EDFF VIS
```

### Noise measurements

After the masks have been created, the noise measurements are performed by the
`measure_skypatch_noise.py` script. This runs a task array to do the measurements
for each combination of field, band and box size.
```
sbatch measure_skypatch_noise.py
```
