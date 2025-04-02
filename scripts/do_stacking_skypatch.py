"""Perform stacking for the skypatch."""

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

name = "sky_patch"
cutout_size = 1.5 * u.deg
ra = 58.7 * u.deg
dec = -50.1 * u.deg

def main():
    in_path = default_data_path("Q1_R1_processed_v0.7", "persistence")
    out_path = default_data_path("Q1_R1_clusters_v0.7", "sky_patch")
    cutout_cen = SkyCoord(ra, dec, frame="icrs")
    try_combine(name=name, cutout_cen=cutout_cen, cutout_size=cutout_size,
                in_dir=in_path, out_dir=out_path, pixel_scale=0.3, bkg_sub=True)
    try_combine(name=f"{name}_no_bkg", cutout_cen=cutout_cen, cutout_size=cutout_size,
                in_dir=in_path, out_dir=out_path, pixel_scale=0.3, bkg_sub=False)

if __name__ == '__main__':
    main()
