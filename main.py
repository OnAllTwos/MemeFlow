import sys
from pathlib import Path
from MemePy.MemeGenerator import add_external_resource_dir

plugindir = Path.absolute(Path(__file__).parent)
paths = (".", "lib", "plugin")
sys.path = [str(plugindir / p) for p in paths] + sys.path

from plugin.meme_flow import MemeFlow

add_external_resource_dir(str(plugindir / "custom_templates"))

if __name__ == "__main__":
    MemeFlow()