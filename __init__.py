# __init__.py
#
# Place this file inside your ComfyUI/custom_nodes/VAE-Decode-Switch/ directory.

import os

# Get the directory of the current file
NODE_DIR = os.path.dirname(__file__)
# Name of the folder containing our JS files
WEB_DIRECTORY = "js"

# Import the node mappings from our python file.
from .vae_decode_switcher import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Tell ComfyUI that this custom node has web assets to load.
# The __all__ list is what ComfyUI's loader looks for.
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
