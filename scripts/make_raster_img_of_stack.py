#!/usr/bin/env python3
# should run in the icl environment
# fmt: off
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=30
#SBATCH --mem=100g
#SBATCH --time=2:00:00
#SBATCH --job-name=make_png
#SBATCH --output=/gpfs01/home/ppzhg/logs/make_png/%j.out
#SBATCH --error=/gpfs01/home/ppzhg/logs/make_png/%j.err
# fmt: on

import argparse
import warnings
from functools import partial
from multiprocessing import Pool
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from astropy.nddata import block_reduce
from astropy.utils.exceptions import AstropyUserWarning
from astropy.visualization import ImageNormalize

from nicl.utilities import sigma_clip_stats

# 1) Suppress the sigma_clip NaN/Infs warning
warnings.filterwarnings(
    "ignore",
    "Input data contains invalid values.*",
    category=AstropyUserWarning,
)

# 2) Suppress the “mean of empty slice” numpy warning
warnings.filterwarnings(
    "ignore",
    "Mean of empty slice.*",
    category=RuntimeWarning,
)


def make_png(path, block_size):
    data = fits.getdata(path, 1)
    data_ = block_reduce(data, block_size, np.nanmean)
    bkg, _, std, _ = sigma_clip_stats(data_, sigma=3, maxiters=30)
    norm = ImageNormalize(
        vmin=bkg - 3 * std,
        vmax=bkg + 3 * std,
    )
    cmap = plt.get_cmap("gray")
    cmap.set_bad("red")
    dpi = 200  # fixed dpi
    fig_width = data_.shape[1] / dpi
    fig_height = data_.shape[0] / dpi
    fig, ax = plt.subplots()
    # set figure size according to the data size
    fig.set_size_inches(fig_width, fig_height)
    fig.set_dpi(dpi)
    ax.imshow(data, cmap=cmap, origin="lower", norm=norm)
    ax.axis("off")
    outpath = path.with_suffix(".png")
    fig.savefig(outpath, dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Produce raster images with a given block size for all stacks in a given folder."
    )
    parser.add_argument(
        "dir", type=str, help="Path to the directory containing the FITS files."
    )
    parser.add_argument(
        "block_size", type=int, help="Block size for the raster images."
    )
    args = parser.parse_args()
    paths = list(Path(args.dir).expanduser().glob("**/EUC_*-STK*.fits"))
    with Pool(30) as pool:
        pool.map(partial(make_png, block_size=args.block_size), paths)
