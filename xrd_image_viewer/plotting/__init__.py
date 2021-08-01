import matplotlib.cm as cm
from ..hdfdata import HdfData

class DataPlotter:
    @staticmethod
    def plotpath(path, ax, min, max):
        arr = HdfData.getarrayfrompath(path)
        ax.pcolormesh(arr, cmap = cm.gist_yarg, vmin = min, vmax = max)