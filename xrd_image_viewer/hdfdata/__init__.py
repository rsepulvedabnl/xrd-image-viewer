import h5py
import hdf5plugin
import numpy as np

class HdfData:
    @staticmethod
    def getarrayfrompath(fpath):
        hfile = h5py.File(fpath, "r")
        data = hfile["/entry/data/data"]
        npdata = np.array(data)
        arr = npdata[0,:,:]

        return arr

    @staticmethod
    def getarrayfrompathwithindex(fpath, idx):
        hfile = h5py.File(fpath, "r")
        data = hfile["/entry/data/data"]
        npdata = np.array(data)
        arr = npdata[idx,:,:]

        return arr