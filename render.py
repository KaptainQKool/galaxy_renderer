from galaxy_renderer.config import PRESETS, preset
from galaxy_renderer import renderer as gr
import star_catalogues as sc
import argparse

gr.render_frames(preset, **{**PRESETS[''], **PRESETS[preset]})