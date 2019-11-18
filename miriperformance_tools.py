import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
from glob import glob
import astropy.units as u


def load_data(version=None, mode=None, extended=False):

    '''Function that will load in ETC data on MIRI performance.
    
    Parameters
    ----------
    - version (string): ETC version
    - pre14 (boolean): is the ETC version earlier than v1.4? [default: False]
    - mode (string): what MIRI mode do we want? (options: 'imager', 'lrs', 'mrs')
    - extended (boolean): do you want numbers for extended sources? (default: False)
    
    Notes:
    ------
    - extended = True is incompatible with line = True
    - by default, all filters will be loaded and plotted for Imager, and all channels and sub-channels for MRS
    
    Output:
    -------
    - data: a dictionary object with the requested values
    
    '''
    
    # initial checks
    assert mode in ['imaging', 'lrs', 'mrs'], "Mode not recognised"
        
    # identify the data directory from the provided ETC version
    data_dir = './data_files/ETC{}/'.format(version.strip())
    assert os.path.isdir(data_dir), "Data directory not found"
    
    # now find the appropriate file
    if extended:
        fname = 'miri_{}_sensitivity_extended*.npz'.format(mode)
    else:
        fname = 'miri_{}_sensitivity.npz'.format(mode)
    
    f = glob(data_dir+fname)
    print(f)
    
    # check that there's only 1 file matching this pattern
    assert len(f)==1, "No single file match"
    
    # now load the file
    data = np.load(f[0], encoding='bytes', allow_pickle=True)
    list(data.keys())
    
    return data


    