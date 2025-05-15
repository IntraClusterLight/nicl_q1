from astropy.table import Table
from matplotlib import pyplot as plt
from nicl.euclid.utilities import default_data_path
from nicl.euclid.background_stats import background_stats_plot

processing_version = "v0.7"

for release_name in ["Q1_R1", "OTF"]:
    path = default_data_path(f"{release_name}_processed_{processing_version}")
    path = path / "stacked_nobkg" / "VIS"
    fns = path.glob("*/background_stats/*.fits")

    for fn in fns:
        outfn = fn.with_suffix(".pdf")
        print(fn, outfn)
        ext_results = Table.read(fn)
        background_stats_plot(ext_results, zp_mag=18.9, filename=outfn, errorbars=True)
        plt.close("all")
