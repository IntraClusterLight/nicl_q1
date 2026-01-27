# Scripts for creating the Q1 skypatch images

## Outline

The scripts in this folder create the Q1 skypatch images for each field and band by
stacking already-processed observations.

In addition to the standard processing, we also create variants in which no processing
is performed and a stack of the MER tiles.

The resulting images are save in folders named after each variant, under the
`Q1_R1_clusters_v1.0/skypatch` folder.

## Data setup

We assume that the processing has already been run for the Q1 observations, and the
processed data is stored in the `Q1_R1_processed_v0.7` folder.

The description below assumes we are submitting SLURM jobs on the Ada supercomputer, but
the scripts can be run individually by omitting the `sbatch` command.


## Running the skypatch stacking


The stacking is performed by the `stack.py` script, for a specified filter and processing
variant.

The `submit_stack_jobs.sh` script submits the stack jobs for each filter and variant.
```
./submit_stack_jobs.sh
```
