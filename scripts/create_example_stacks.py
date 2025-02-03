from astropy.coordinates import SkyCoord
from astropy import units as u

from nicl.utilities import physical_to_angular
from nicl.euclid.utilities import default_data_path
from nicl.euclid.combine import combine

cluster_id = "MCXCJ1754.6+6803"
z = 0.07
ra = 268.662 * u.deg
dec = 68.058 * u.deg
cutout_radius_physical = 500 * u.kpc
cutout_radius_angular = physical_to_angular(cutout_radius_physical, z)
cutout_size = 4 * cutout_radius_angular

in_dir = default_data_path("Q1_R1")
out_dir = default_data_path("Q1_R1_clusters_test", cluster_id, "original")

#combine(
#    in_dir=in_dir,
#    out_dir=out_dir,
#    add_bkg_mod=True,
#    cutout_cen=SkyCoord(ra, dec),
#    cutout_size=cutout_size,
#    name=cluster_id,
#    filters=["H", "VIS", "NIR-H"],
#    pixel_scale=0.3,
#    overwrite=True,
#)

# combine(
#    in_dir=in_dir,
#    out_dir=out_dir,
#    add_bkg_mod=False,
#    cutout_cen=SkyCoord(ra, dec),
#    cutout_size=cutout_size,
#    name=cluster_id,
#    filters=["NIR-H"],
#    pixel_scale=0.3,
#    overwrite=True,
# )
 
#for variant in ("_no_debanding", "_no_skyflat_no_debanding", "_no_skyflat"):
for variant in ("persistence_no_skyflat",):
    in_dir = default_data_path("Q1_R1_processed_test", f"{variant}")
    out_dir = default_data_path("Q1_R1_clusters_test", cluster_id, f"{variant.replace('persistence_', '')}")
    combine(
        in_dir=in_dir,
        out_dir=out_dir,
        cutout_cen=SkyCoord(ra, dec),
        cutout_size=cutout_size,
        name=cluster_id,
        filters=["H"],
        pixel_scale=0.3,
        overwrite=True,
    )

# in_dir = default_data_path("Q1_R1_processed_test", "persistence")
# out_dir = default_data_path("Q1_R1_clusters_test", cluster_id, f"no_background")
# combine(
#     in_dir=in_dir,
#     out_dir=out_dir,
#     bkg_sub=False,
#     cutout_cen=SkyCoord(ra, dec),
#     cutout_size=cutout_size,
#     name=cluster_id,
#     filters=["H"],
#     pixel_scale=0.3,
#     overwrite=True,
# )
