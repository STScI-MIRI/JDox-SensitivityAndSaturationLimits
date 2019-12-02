import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
from glob import glob
import astropy.units as u


def load_data(version=None, mode=None, src=None):

    '''Function that will load in ETC data on MIRI performance.
    
    Parameters
    ----------
    - version (string): ETC version
    - pre14 (boolean): is the ETC version earlier than v1.4? [default: False]
    - mode (string): what MIRI mode do we want? (options: 'imager', 'lrs', 'mrs')
    - src (string): 'point' or 'extended'?
    
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
    assert src in ['point', 'extended'], "Source type not recognised"
        
    # identify the data directory from the provided ETC version
    data_dir = './data_files/ETC{}/'.format(version.strip())
    assert os.path.isdir(data_dir), "Data directory not found"
    
    # now find the appropriate file
    if src == 'extended':
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

def make_imager_plots(version=None, save=False, outfile='out.png', style='jdocs'):
    
    '''
    Function that will produce plot of sensitivity and bright limits for the imager for both point and extended sources (4 plots in total).
    
    Parameters:
    -----------
    - version (string): version number
    - save (boolean): should the plot be saved to file? default: 'False'
    - outfile (string): output filename. default: 'out.png'
    - style (string): plotting style. default: 'jdocs' -- TO DO
    
    
    '''
    plt.close('all')

    src = ['point', 'extended']
    types = ['sens', 'sat']
    
    #subs = ['ALL', 'FULL', 'BRIGHTSKY', 'SUB256', 'SUB128', 'SUB64']
    #rdtimes = [2.77504, 2.77504, 0.865, 0.300, 0.119, 0.085]
    #rdfac = rdtimes / 2.77504
    #print(rdtimes)
    #assert subarray in subs, "Subarray name not recognised"
    
    sens_label = 'SNR = 10 in 10 ksec'
    sat_label = 'Signal reaching 70% full well in NGROUPS = 5'
    vlabel = 'Generated with ETCv{}'.format(version)
    
    for s in src[:1]:
        data = load_data(version=version, mode='imaging', src=s)
        # first the sensitivity plot
        fig1, ax1 = plt.subplots(figsize=[8,6])
        ax1.semilogy(data['wavelengths'], data['lim_fluxes'], ls='', marker='o', mec='k', mfc='k', ms=14, label='min detectable signal')
        ax1.set_xlabel('wavelength ($\mu$m)', fontsize='large')
        ax1.set_ylabel('flux density (mJy)', fontsize='large')
        ax1.set_title('MIRI Imager sensitivity ({} sources)'.format(s))
        ax1.annotate(sens_label, (20., 1.5e-4), fontsize=10)
        ax1.annotate(vlabel, (20., 1.2e-4), fontsize=10)
        ax1.grid(alpha=0.5, which='both')
        fig1.show()
        if save:
            new_outfile = 'plots/ETC{0}/{1}_{2}_sens.png'.format(version, outfile.split('.')[0], s)
            plt.savefig(new_outfile)
        
        fig2, ax2 = plt.subplots(figsize=[8,6])
        ax2.semilogy(data['wavelengths'], data['sat_limits'], ls='', marker='o', mec='k', mfc='k', ms=14, label='saturation limits')
        ax2.set_xlabel('wavelength ($\mu$m)', fontsize='large')
        ax2.set_ylabel('flux density (mJy)', fontsize='large')
        ax2.set_title('MIRI Imager bright limits ({} sources)'.format(s))
        ax2.annotate(sat_label, (14., 4), fontsize=10)
        ax2.annotate(vlabel, (14., 3.4), fontsize=10)
        ax2.grid(alpha=0.5, which='both')
        fig2.show()
        if save:
            new_outfile = 'plots/ETC{0}/{1}_{2}_sat.png'.format(version, outfile.split('.')[0], s)
            plt.savefig(new_outfile)
            
            
    return
        
        
        
        