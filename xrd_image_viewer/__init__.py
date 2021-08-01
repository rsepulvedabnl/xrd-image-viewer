from .gui import *
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

def launch():
    builder = RootWindowBuilder()
    builder.buildroot()

    win = builder.getroot()
    win.mainloop()