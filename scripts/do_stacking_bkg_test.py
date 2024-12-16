"""Perform stacking for all of Q1 in the default location."""

import os
import sys

from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord

from nicl.euclid.combine import Combiner
from nicl.euclid.utilities import default_data_path

def try_stacking(*args, **kwargs):
    try:
        combiner = Combiner(*args, **kwargs)
        combiner.combine()
    except Exception as e:
        print(e)
        
def main(mesh=0):
    if mesh == 0:
        bkg_sub = False
        bkg_mesh_size = None
    else:
        bkg_sub = True
        # avoid slivers
        bkg_mesh_size = 2041 * 0.3 * u.arcsec / mesh
    print(f"mesh = {mesh}, bkg_mesh_size = {bkg_mesh_size}")
    in_path = default_data_path("Q1_R1_processed_v0.2", "persistence")
    out_path = default_data_path("Q1_R1_clusters_v0.2_bkg_test_nofilter", f"mesh{mesh}")
    clusters = Table.read(default_data_path("catalogs/EDFN_CLUSTERS_LSB_processing_subset.fits"))
    print("Processing:")
    for cluster in clusters:
        print(cluster, flush=True)
        cutout_cen = SkyCoord(cluster["RA"] * u.deg, cluster["DEC"] * u.deg, frame="icrs")
        cutout_size = cluster["boxsize"] * u.arcmin
        try_stacking(name=cluster["Name"], cutout_cen=cutout_cen, cutout_size=cutout_size,
                     bkg_sub=bkg_sub, bkg_mesh_size=bkg_mesh_size, filter_size=1,
                     in_path=in_path, out_path=out_path, filters="H", overwrite=True,
)

if __name__ == '__main__':
    for mesh in range(11):
        main(mesh)
