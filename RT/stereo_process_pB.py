"""
Script for processing polarized brightness (pB) images from STEREO-A/COR2 such that they can be used by the SWPC CME Analysis Tool (CAT).  This is mainly a wrapper for the IDL routine `combine_stereo_pb.pro`, which uses the SolarSoft routine `secchi_prep.pro` to combine three pB images into a total brightness (tB) image.  The resulting image is written as a fits file to a specified output directory.

"""

import glob
import numpy as np
import os
import subprocess

from astropy.io import fits
from astropy.time import Time

red = '\033[91m'
yellow = '\033[93m'
cend = '\033[0m'

def complete_set(files, verbose = True):

    # check for a matching set of polarizations
    pset = [0.0, 120.0, 240.0]

    # and check that all the measurements are within 30 min of each other
    # max allowable time difference, in seconds
    dtmax = 1800.

    if len(files) != 3:
        return (False, None)

    times = []
    pol = []

    if verbose:
        print(80*'-')
    for file in files:
        if verbose:
            print(file)
        hdu = fits.open(file)[0]
        times.append(Time(hdu.header['DATE']).gps)
        pol.append(hdu.header['POLAR'])

    t = np.array(times)
    dt = np.max(t) - np.min(t)

    if all(x in pol for x in pset) and dt < dtmax:
        # complete set!
        # define a mean time to associate with the composite image
        time = Time(0.5*(np.min(t) + np.max(t)), format = 'gps')
        time.format='jd'
        if verbose:
            print(yellow+f"complete set!: {time}"+cend)
        return (True, time)
    else:
        if verbose:
            print(red+f"incomplete set: {pol} {dt/60}"+cend)
        return (False, None)

def process_files(dir, outdir, newfile = None, \
                  sswidl = "/usr/local/ssw/gen/setup/ssw_idl"):

    #------------------------------------------------------------------------------
    # Select three files from the target directory to process
    # Nominal operation is to choose the new file that was most recently added
    # to the directory, plus the two files that precede it, in terms of when
    # the files were created.
    # If something goes wrong with this nominal operation then the default is 
    # just to select the most recent three files in the directory

    files = list(filter(os.path.isfile, glob.glob(dir + "*.fts")))

    if len(files) < 3:
        return(0)

    files.sort(key=lambda x: os.path.getmtime(x))

    try:
        idx = files.index(newfile)
    except:
        idx = len(files) - 1

    f = files[idx-2:idx+1]

    #------------------------------------------------------------------------------
    # if the files form a complete set, then run the procedure

    complete, time = complete_set(f)

    if complete:
        print(yellow+"Creating pB composite file"+cend)

        outfile = outdir + time.strftime('%Y%m%d_%H%M%S'+'_pBcom.fts')
        print(f"outfile = {outfile}")

        idlcommand = f"combine_stereo_pb,'{f[0]}','{f[1]}','{f[2]}','{time.jd}','{outfile}'"
        #subprocess.run([sswidl,"-e",idlcommand], env=os.environ)

    return(0)

    #------------------------------------------------------------------------------

