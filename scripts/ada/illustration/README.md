# Scripts for illustrating the post-processing steps

## Outline

The scripts in this folder run the nicl NIR post-processing to illustrate the effect of
each element of the processing, in terms of removing artefacts and flattening
the background. Observation 2683 is processed through the standard v1.0 pipeline, as
well as variants in which a single element of the processing is removed, and a variant
without any processing (other than stacking).

In addition to the individual processed dithers, we make a combined image centred on the
cluster MCXCJ1754.6+6803 for each variant.

The resulting images are save in folders named after each variant, under the
`Q1_R1_processed_illustration/ablation` folder.

We also run the persistence correction with debug output for a single detector chip.
The output for this is saved in the `Q1_R1_processed_illustration/persistence` folder.


## Data setup

We assume that skyflats have already been prepared in `Q1_R1_processed_v0.7`.

The description below assumes we are submitting SLURM jobs on the Ada supercomputer, but
the scripts can be run individually by omitting the `sbatch` command.


## Running the processing

### NIR processing

The NIR processing is performed by the `run_processing_nir.py` script.
This takes options to skip various steps of the processing, for ablation studies.

The `submit_processing_jobs.sh` script submits the processing jobs for each variant.
```
./submit_processing_jobs.sh
```

### NIR processing with debug output

The NIR processing with debug output is performed by the `run_processing_nir_debug.py` script,
which can be submitted with the following command:
```
sbatch run_processing_nir_debug.py
```


### Stacking the clusters

The stacking is performed by the `stack.py` script, for a specified filter andprocessing
variant. The script `stack.sh` is used to submit a SLURM job array for a specified filter
and variant.

The `submit_stack_jobs.sh` script submits the stack jobs for each filter and variant.
```
./submit_stack_jobs.sh
```
