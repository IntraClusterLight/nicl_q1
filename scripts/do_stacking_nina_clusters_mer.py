"""Perform stacking for Nina's clusters."""

from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord

from nicl.euclid.combine import combine
from nicl.euclid.utilities import default_data_path

def try_combine(*args, **kwargs):
    name = kwargs["name"]
    try:
        print(f"Processing {name}...", flush=True)
        combine(*args, **kwargs)
        print(f"Completed {name}...", flush=True)
    except Exception as e:
        print("Exception in combine:", e)
        
def main():
    clusters = Table.read(default_data_path("catalogs/EDFN_CLUSTERS_LSB_processing_subset.fits"))
    in_path = default_data_path("Q1_R1", "MER")
    out_path = default_data_path("Q1_R1_clusters_v0.4", f"nina_mer")
    for cluster in clusters:
        cutout_cen = SkyCoord(cluster["RA"] * u.deg, cluster["DEC"] * u.deg, frame="icrs")
        cutout_size = cluster["boxsize"] * u.arcmin
        try_combine(name=cluster["Name"], cutout_cen=cutout_cen, cutout_size=cutout_size,
                    in_dir=in_path, out_dir=out_path, filters="NIR-H", bkg_sub=True)

if __name__ == '__main__':
    main()
