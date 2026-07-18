from astropy.visualization import make_lupton_rgb
from typing import Iterator, Any
import matplotlib.pyplot as plt
import star_catalogues as sc
from pathlib import Path
import matplotlib as mpl
import pandas as pd
import json


def render_frames():
    return


def draw(rgb: list[list[list[float]]], resolution: list[int], filename: str):
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.]) # shut up type checker
    fig.set_size_inches(resolution[0], resolution[1])
    ax.set_axis_off()
    ax.set_aspect('auto')
    fig.add_axes(ax)
    image = make_lupton_rgb(rgb[:][:][0], rgb[:][:][1], rgb[:][:][2])
    plt.imshow(image)
    plt.savefig(filename, dpi=1)
    # plt.show()