import os
from importlib import reload
from . import *


def _reload_modules():
    reload(preferences)

_DEV_MODE = bool(os.environ.get('BLENDER_DEV_MODE', 0))
reload_modules = _reload_modules if _DEV_MODE else lambda: None
