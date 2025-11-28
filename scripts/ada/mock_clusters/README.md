# Scripts for full processing of mock cluster observations

## Outline

The scripts in this folder run the nicl post-processing and profile measurement for
testing purposes. The primary goal is to check that the various elements of the
processing do not remove any flux for sources extended on a scale of a few arcmin.
In addition, the different variants of the processing illustrate the benefit of
each element of the processing, in terms of removing artefacts and flattening
the background.

The standard test cluster image created by `nicl.euclid.testing` is injected
into a set of observations at four positions, listed in `mock_clusters.txt`. The
observations are then processed through the standard v1.0 pipeline, as well as
variants in which a single element of the processing is removed, and a variant
without any processing (other than stacking).

The resulting images of each mock cluster (in the `Q1_R1_mock_clusters_v1.0`
folder) and their profiles (in the `Q1_R1_mock_clusters_v1.0_measurements` folder)
may be compared to the original test cluster image (in the `test_images` folder)
and profile (in the `test_measurements` folder). Note that the injected profile
has been convolved with the Euclid ERO PSF (in the `ERO_PSFs` folder).


## Data setup

To begin, the data must be prepared. The data in the folder `~/euclid_data/Q1_R1_mock_clusters`
is symlinked to the original Q1_R1 data, except for observations 3582, 3583, 3590, 3591, 3592,
3593, 3594, which are replaced by a version of the original data with the mock clusters injected.

```shell
cd ~/euclid_data
mkdir Q1_R1_mock_clusters
cd Q1_R1_mock_clusters
mkdir SIR
mkdir NIR
mkdir VIS_QUAD
cd SIR
ln -s ../../Q1_R1/SIR/* .
cd ..
cd NIR
ln -s ../../Q1_R1/NIR/* .
for obs_id in 3582 3583 3590 3591 3592 3593 3594; do
    rm -f $obs_id
    mkdir $obs_id
    cd $obs_id
    cp -p ../../../LSB_sim_outputs_4_clusters/*NIR*${obs_id}-*_LSBSim.fits .
    for f in *_LSBSim*; do mv "$f" "${f/_LSBSim/}"; done
    cd ..
done
cd ..
cd VIS_QUAD
ln -s ../../Q1_R1/VIS_QUAD/* .
for obs_id in 3582 3583 3590 3591 3592 3593 3594; do
    rm -f $obs_id
    mkdir $obs_id
    cd $obs_id
    cp -p ../../../LSB_sim_outputs_4_clusters/*VIS*${obs_id}-*_LSBSim.fits .
    for f in *_LSBSim*; do mv "$f" "${f/_LSBSim/}"; done
    cd ..
done
cd ..
```

To save time, the zarr folder can be created in `Q1_R1_mock_clusters_processed_v1.0`,
with symlinks to the Q1_R1_processed_v0.7/zarr folder, except for the replaced observations.

```shell
cd ~/euclid_data
mkdir Q1_R1_mock_clusters_processed_v1.0
cd Q1_R1_mock_clusters_processed_v1.0
mkdir zarr
cd zarr
mkdir NIR
cd NIR
ln -s ../../../Q1_R1_processed_v0.7/zarr/Q1_R1/NIR/* .
rm -f 3582 3583 3590 3591 3592 3593 3594
cd ..
mkdir VIS
cd VIS
ln -s ../../../Q1_R1_processed_v0.7/zarr/Q1_R1/VIS/* .
rm -f 3582 3583 3590 3591 3592 3593 3594
cd ../../..
```

The description below assumes we are submitting SLURM jobs on the Ada supercomputer, but
the scripts can be run individually by omitting the `sbatch` command.


## Running the processing

### Skyflats

The skyflat for the replaced observations must first be created. 
```
sbatch run_skyflats_nir.py
sbatch run_skyflats_vis.py
```

### NIR processing

The NIR processing is performed by the `run_processing_nir.py` script.
This takes options to skip various steps of the processing, for ablation studies.

The `submit_processing_jobs.sh` script submits the processing jobs for each variant.
```
. submit_processing_jobs.sh
```

### Stacking the clusters

The stacking is performed by the `stack.py` script, for a specified filter, processing
variant and cluster index in the `mock_clusters.txt` file.
The script `stack.sh` is used to submit a SLURM job array for a specified filter and variant.

The `submit_stack_jobs.sh` script submits the stack jobs for each filter and variant.
```
. submit_stack_jobs.sh
```

### Measuring the profiles

The various steps for measuring the profiles are performed by the `measure.py` script.
The script `submit_measure.sh` is used to submit a set of interdependent jobs to measure
the profiles for a single cluster.


The `submit_measure.py` script submits the jobs for each cluster, for a single specified
processing variant.
```
python submit_measure.py
python submit_measure.py --variant no_skyflat
python submit_measure.py --variant no_tartan
python submit_measure.py --variant no_persistence
python submit_measure.py --variant no_bkg_match
python submit_measure.py --variant no_processing
```
