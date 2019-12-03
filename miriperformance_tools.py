import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
from glob import glob
import astropy.units as u

plt.style.use('seaborn-colorblind')

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
    Function that will produce plot of sensitivity and bright limits for the imager for both point and extended sources (2 plots in total).
    
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
    
    ylab = ['flux density (mJy)', 'surface brightness (mJy arcsec$^{-2}$)']
    
    for s, yl in zip(src, ylab):
        data = load_data(version=version, mode='imaging', src=s)
        # first the sensitivity plot
        fig1, ax1 = plt.subplots(figsize=[8,6])
        ax1.semilogy(data['wavelengths'], data['lim_fluxes'], ls='', marker='o', ms=12, label='min detectable signal')
        #ax1.semilogy(data['wavelengths'], data['lim_fluxes'], ls='', label='min detectable signal')
        ax1.set_xlabel('wavelength ($\mu$m)')
        ax1.set_ylabel(yl)
        ax1.set_title('MIRI Imager sensitivity ({} sources)'.format(s))
        ax1.annotate(sens_label, (0.7,0.15), fontsize=9, xycoords='figure fraction')
        ax1.annotate(vlabel, (0.7,0.12), fontsize=9, xycoords='figure fraction')
        ax1.grid(b=True)
        fig1.show()
        if save:
            new_outfile = 'plots/ETC{0}/{1}_{2}_sens.png'.format(version, outfile.split('.')[0], s)
            plt.savefig(new_outfile)
        
        fig2, ax2 = plt.subplots(figsize=[8,6])
        ax2.semilogy(data['wavelengths'], data['sat_limits'], ls='', marker='o', ms=12, label='saturation limits')
        #ax2.semilogy(data['wavelengths'], data['sat_limits'], ls='', label='saturation limits')
        ax2.set_xlabel('wavelength ($\mu$m)')
        ax2.set_ylabel(yl)
        ax2.set_title('MIRI Imager bright limits ({} sources)'.format(s))
        ax2.annotate(sat_label, (0.5, 0.15), fontsize=9, xycoords='figure fraction')
        ax2.annotate(vlabel, (0.5, 0.12), fontsize=9, xycoords='figure fraction')
        ax2.grid(b=True)
        fig2.show()
        if save:
            new_outfile = 'plots/ETC{0}/imager_{1}_{2}_sat.png'.format(version, outfile.split('.')[0], s)
            plt.savefig(new_outfile)
            
            
    return
        
        
def make_lrs_plots(version=None, save=False, outfile='out.png', style='jdocs'):
    
    '''
    Function that will produce plot of sensitivity and bright limits for the LRS for both point and extended sources (4 plots in total).
    
    Parameters:
    -----------
    - version (string): version number
    - save (boolean): should the plot be saved to file? default: 'False'
    - outfile (string): output filename. default: 'out.png'
    - style (string): plotting style. default: 'jdocs' -- TO DO
    
    
    '''
    plt.close('all')
    
    # LRS only has point source numbers
    src = ['point']
    types = ['sens', 'sat']
    
    #subs = ['ALL', 'FULL', 'BRIGHTSKY', 'SUB256', 'SUB128', 'SUB64']
    #rdtimes = [2.77504, 2.77504, 0.865, 0.300, 0.119, 0.085]
    #rdfac = rdtimes / 2.77504
    #print(rdtimes)
    #assert subarray in subs, "Subarray name not recognised"
    
    sens_label = 'SNR = 10 in 10 ksec'
    sat_label = 'Signal reaching 70% full well in NGROUPS = 5'
    vlabel = 'Generated with ETCv{}'.format(version)
    frame_ratio = 0.159 / 2.7705
    
    for s in src:
        data = load_data(version=version, mode='lrs', src=s)
        print(data['configs'])
        # first the sensitivity plot
        fig1, ax1 = plt.subplots(figsize=[8,6])
        ax1.semilogy(data['wavelengths'][1], data['lim_fluxes'][1], ls='-', lw=2, label='slit')
        ax1.semilogy(data['wavelengths'][0], data['lim_fluxes'][0], ls='-', lw=2, label='slitless')
        ax1.set_xlabel('wavelength ($\mu$m)', fontsize='large')
        ax1.set_ylabel('flux density (mJy)', fontsize='large')
        ax1.set_title('MIRI LRS sensitivity (point sources)'.format(s))
        ax1.annotate(sens_label, (0.7, 0.15), fontsize=9, xycoords='figure fraction')
        ax1.annotate(vlabel, (0.7, 0.12), fontsize=10, xycoords='figure fraction')
        ax1.grid(alpha=0.5, which='both')
        ax1.legend(loc='best', fontsize='large')
        fig1.show()
        if save:
            new_outfile = 'plots/ETC{0}/lrs_{1}_{2}_sens.png'.format(version, outfile.split('.')[0], s)
            plt.savefig(new_outfile)
        
        fig2, ax2 = plt.subplots(figsize=[8,6])
        ax2.semilogy(data['wavelengths'][1], data['sat_limits'][1], ls='-', lw=2, label='slit')
        ax2.semilogy(data['wavelengths'][0], data['sat_limits'][0] / frame_ratio, ls='-', lw=2, label='slitless')
        ax2.set_xlabel('wavelength ($\mu$m)', fontsize='large')
        ax2.set_ylabel('flux density (mJy)', fontsize='large')
        ax2.set_title('MIRI LRS bright limits ({} sources)'.format(s))
        ax2.annotate(sat_label, (9., 2.4), fontsize=10)
        ax2.annotate(vlabel, (9., 1.5), fontsize=10)
        ax2.grid(alpha=0.5, which='both')
        ax2.legend(loc='best', fontsize='large')
        fig2.show()
        if save:
            new_outfile = 'plots/ETC{0}/lrs_{1}_{2}_sat.png'.format(version, outfile.split('.')[0], s)
            plt.savefig(new_outfile)
            
            
    return



def make_mrs_plots(version=None, save=False, outfile='out.png', style='jdocs'):
    
    '''
    Function that will produce plot of sensitivity and bright limits for the LRS for both point and extended sources (4 plots in total).
    
    Parameters:
    -----------
    - version (string): version number
    - save (boolean): should the plot be saved to file? default: 'False'
    - outfile (string): output filename. default: 'out.png'
    - style (string): plotting style. default: 'jdocs' -- TO DO
    
    
    '''
    plt.close('all')
    
    
    # LRS only has point source numbers
    src = ['point', 'extended']
    types = ['sens', 'sat']
    ylab = ['flux density (mJy)', 'surface brightness (mJy arcsec$^{-2}$)']
    
    ishort = [0, 3, 6, 9]
    imed = [i + 1 for i in ishort]
    ilong = [i + 2 for i in ishort]
    mrslabs = ['MRS short', '', '', '', 'MRS medium', '', '', '', 'MRS long', '', '', '']
    
    # Parsing for each channel
    ichan1 = [0, 1, 2]                        #S,M,L
    ichan2 = [i + 3 for i in ichan1]
    ichan3 = [i + 3 for i in ichan2]
    ichan4 = [i + 3 for i in ichan3]
    
    
    sens_label = 'SNR = 10 in 10 ksec'
    sat_label = 'Signal reaching 70% full well in NGROUPS = 5'
    vlabel = 'Generated with ETCv{}'.format(version)
    frame_ratio = 0.159 / 2.7705
    
    for s, yl in zip(src, ylab):
        data = load_data(version=version, mode='mrs', src=s)
        #print(list(data.keys()))
        # first the sensitivity plot
        fig1, ax1 = plt.subplots(figsize=[8,6])
        for sh in ishort:
            ax1.semilogy(data['wavelengths'][sh], data['lim_fluxes'][sh], lw=2, label = mrslabs[sh])
        for m in imed:
            ax1.semilogy(data['wavelengths'][m], data['lim_fluxes'][m], lw=2, label = mrslabs[m])
        for l in ilong:
            ax1.semilogy(data['wavelengths'][l], data['lim_fluxes'][l], lw=2, label = mrslabs[l])
        
        
        #ax1.set_xlabel('wavelength ($\mu$m)', fontsize='large')
        ax1.set_xlabel('wavelength ($\mu$m)')
        ax1.set_ylabel(yl, fontsize='large')
        ax1.set_title('MIRI MRS continuum sensitivity ({} sources)'.format(s))
        ax1.annotate(sens_label, (0.7,0.15), fontsize=9, xycoords='figure fraction')
        ax1.annotate(vlabel, (0.7, 0.12), fontsize=9, xycoords='figure fraction')
        ax1.grid(alpha=0.5, which='both')
        ax1.legend(loc='best', fontsize='large')
        fig1.show()
        if save:
            new_outfile = 'plots/ETC{0}/mrs_{1}_{2}_sens.png'.format(version, outfile.split('.')[0], s)
            plt.savefig(new_outfile)
        
        fig2, ax2 = plt.subplots(figsize=[8,6])
        for sh in ishort:
            ax2.semilogy(data['wavelengths'][sh], data['sat_limits'][sh], lw=2, label = mrslabs[sh])
        for m in imed:
            ax2.semilogy(data['wavelengths'][m], data['sat_limits'][m], lw=2,  label = mrslabs[m])
        for l in ilong:
            ax2.semilogy(data['wavelengths'][l], data['sat_limits'][l], lw=2,  label = mrslabs[l])
        ax2.set_xlabel('wavelength ($\mu$m)', fontsize='large')
        ax2.set_ylabel(yl, fontsize='large')
        ax2.set_title('MIRI MRS bright limits ({} sources)'.format(s))
        #ax2.annotate(sat_label, (17.5, 1.8e4), fontsize=9, xycoords='figure fraction')
        ax2.annotate(sat_label, (0.5,0.15), fontsize=9, xycoords='figure fraction')
        #ax2.annotate(vlabel, (17.5, 1.5e4), fontsize=9)
        ax2.annotate(vlabel, (0.5, 0.12), fontsize=9, xycoords='figure fraction')
        ax2.grid(alpha=0.5, which='both')
        ax2.legend(loc='best', fontsize='large')
        fig2.show()
        if save:
            new_outfile = 'plots/ETC{0}/mrs_{1}_{2}_sat.png'.format(version, outfile.split('.')[0], s)
            plt.savefig(new_outfile)
            
            
    return
    
    
def sens_plot(version=None, save=False, outfile='out.png', style='jdocs'):
    
    '''
    Function that will produce plot of sensitivity plots both point and extended sources, for imager, LRS and MRS.
    
    Parameters:
    -----------
    - version (string): version number
    - save (boolean): should the plot be saved to file? default: 'False'
    - outfile (string): output filename. default: 'out.png'
    - style (string): plotting style. default: 'jdocs' -- TO DO
    
    
    '''
    plt.close('all')
    
    ishort = [0, 3, 6, 9]
    imed = [i + 1 for i in ishort]
    ilong = [i + 2 for i in ishort]
    mrslabs = ['MRS short', '', '', '', 'MRS medium', '', '', '', 'MRS long', '', '', '']
    
    modes = ['imaging', 'lrs', 'mrs']
    
    # LRS only has point source numbers
    src = ['point', 'extended']
    ylab = ['flux density (mJy)', 'surface brightness (mJy arcsec$^{-2}$)']
    sens_label = 'SNR = 10 in 10 ksec'
    vlabel = 'Generated with ETCv{}'.format(version)
    
    fig, ax = plt.subplots(figsize=[8,6])
    
    for m in modes:
        data = load_data(mode=m, version=version, src='point')
        if m == 'imaging':
            ax.semilogy(data['wavelengths'], data['lim_fluxes'], ls = '', marker='o', ms=10, label='imager')
        elif m == 'lrs':
            ax.semilogy(data['wavelengths'][0], data['lim_fluxes'][0], lw=2, label='LRS slitless')
            ax.semilogy(data['wavelengths'][1], data['lim_fluxes'][1], lw=2, label='LRS slit')
        else:
            for sh in ishort:
                ax.semilogy(data['wavelengths'][sh], data['lim_fluxes'][sh], lw=2, c='#56B4E9', label = mrslabs[sh])
            for m in imed:
                ax.semilogy(data['wavelengths'][m], data['lim_fluxes'][m], lw=2, c='#CC79A7', label = mrslabs[m])
            for l in ilong:
                ax.semilogy(data['wavelengths'][l], data['lim_fluxes'][l], lw=2, c='#F0E442', label = mrslabs[l])
    ax.set_xlabel('wavelength ($\mu$m)')
    ax.set_ylabel('flux density (mJy)', fontsize='large')
    ax.set_title('MIRI point source sensitivities (continuum)')
    ax.annotate(sens_label, (0.7,0.15), fontsize=9, xycoords='figure fraction')
    ax.annotate(vlabel, (0.7, 0.12), fontsize=9, xycoords='figure fraction')
    ax.grid(alpha=0.5, which='both')
    ax.legend(loc='best', fontsize='large')
    fig.show()
    
    if save:
        new_outfile = 'plots/ETC{0}/sens_all_point_v{0}.png'.format(version)
        plt.savefig(new_outfile)
    return 
    
def bright_plot(version=None, save=False, outfile='out.png', style='jdocs'):
    
    '''
    Function that will produce plot of bright limits plots both point and extended sources, for imager, LRS and MRS.
    
    Parameters:
    -----------
    - version (string): version number
    - save (boolean): should the plot be saved to file? default: 'False'
    - outfile (string): output filename. default: 'out.png'
    - style (string): plotting style. default: 'jdocs' -- TO DO
    
    
    '''
    plt.close('all')
    
    ishort = [0, 3, 6, 9]
    imed = [i + 1 for i in ishort]
    ilong = [i + 2 for i in ishort]
    mrslabs = ['MRS short', '', '', '', 'MRS medium', '', '', '', 'MRS long', '', '', '']
    
    modes = ['imaging', 'lrs', 'mrs']
    
    frame_ratio = 0.159 / 2.7705
    
    # LRS only has point source numbers
    src = ['point', 'extended']
    ylab = ['flux density (mJy)', 'surface brightness (mJy arcsec$^{-2}$)']
    sat_label = 'Signal reaching 70% full well in NGROUPS = 5'
    vlabel = 'Generated with ETCv{}'.format(version)
    
    fig, ax = plt.subplots(figsize=[8,6])

    
    im = load_data(mode='imaging', version=version, src='point')
    ax.semilogy(im['wavelengths'], im['sat_limits'], ls = '', marker='o', ms=10, label='imager')
    lrs = load_data(mode='lrs', version=version, src='point')
    ax.semilogy(lrs['wavelengths'][0], lrs['sat_limits'][0] / frame_ratio, lw=2, label='LRS slitless')
    ax.semilogy(lrs['wavelengths'][1], lrs['sat_limits'][1], lw=2, label='LRS slit')
    mrs = load_data(mode='mrs', version=version, src='point')
    for sh in ishort:
        ax.semilogy(mrs['wavelengths'][sh], mrs['sat_limits'][sh], c='#56B4E9', label = mrslabs[sh])
    for m in imed:
        ax.semilogy(mrs['wavelengths'][m], mrs['sat_limits'][m], c='#CC79A7',  label = mrslabs[m])
    for l in ilong:
        ax.semilogy(mrs['wavelengths'][l], mrs['sat_limits'][l], c='#F0E442',  label = mrslabs[l])
    ax.set_xlabel('wavelength ($\mu$m)')
    ax.set_ylabel('flux density (mJy)', fontsize='large')
    ax.set_title('MIRI point source bright limits (continuum)')
    ax.annotate(sat_label, (0.5,0.15), fontsize=9, xycoords='figure fraction')
    ax.annotate(vlabel, (0.5, 0.12), fontsize=9, xycoords='figure fraction')
    #ax.grid(alpha=0.5, which='both')
    ax.legend(loc='best')
    fig.show()
    
    if save:
        new_outfile = 'plots/ETC{0}/bright_all_point_v{0}.png'.format(version)
        plt.savefig(new_outfile)
    return 
    
    
    
    
    
        
        
        