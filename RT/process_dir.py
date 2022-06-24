
import glob
import numpy as np
import os
import subprocess

from astropy.io import fits
from astropy.time import Time
from stereo_process_pB import complete_set

"""
This function is for processing STEREO-A polarized brightness (pB) file in "batch" mode.  It processes all files in a specified target directory.  It starts by generating a file list for the target directory, then it loops through all files in the directory looking for two other files that form a complete set.

A complete set consists of three observations with different polarization states (0, 120, and 240) all taken within 30 minutes of one another.  If a complete set is found, the three pB images are processed with the SolarSoft `secchi_prep` function and the images are combined to form a total brightness (tB) image.   This tB image is written as a fits file to a specified output directory.  The output file name reflects the date of the observation and includes the tag `pBcom` to represent a polarized brightness composite.

This function is used to process all files in the target directory.  So, if files come in one at a time throughout the course of a day and are written to the target directory, then this function will do unneccesary work.  It will process all the earlier files again.

If the pB (seq) files arrive one at a time then the `watch_dir.py` function should be used instead of this one.  It is expected that `watch_dir.py` will be the primary function for operational use.  This function is provided mainly as a utility, for manual operation in case something goes wrong with the nominal operational process.

"""
#------------------------------------------------------------------------------
red = '\033[91m'
yellow = '\033[93m'
cend = '\033[0m'

#------------------------------------------------------------------------------
# define platform-specific parameters

# this is the directory to monitor for new files
targetdir = '../data/seq/'
#targetdir = '../data/tmp/'

#output directory
outdir = '../data/pBcom/'

# location of sswidl executable
sswidl = "/usr/local/ssw/gen/setup/ssw_idl"

#------------------------------------------------------------------------------
# define platform-agnostic parameters
# make sure these are consistent with the `complete_set` function in
# `stereo_process_pB.py`

pset = [0.0, 120.0, 240.0]

# max allowable time difference, in seconds
dtmax = 1800.

#------------------------------------------------------------------------------
# check input specification

if targetdir[-1] != '/':
    print(red+"Error: target directory must end in '/'"+cend)
    exit(1)

if outdir[-1] != '/':
    print(red+"Error: output directory must end in '/'"+cend)
    exit(1)

if not os.path.exists(outdir):
    os.mkdir(outdir)

#------------------------------------------------------------------------------
# first get the file list of the target directory

files = list(filter(os.path.isfile, glob.glob(targetdir + "*.fts")))

if len(files) < 3:
    exit(0)

files.sort(key=lambda x: os.path.getmtime(x))

#------------------------------------------------------------------------------
# now loop over files, looking for a complete set

# remaining files to be processed
filelist = files.copy()

for file in files:

    #print(yellow+f"{file} {len(filelist)}"+cend)

    hdu = fits.open(file)[0]
    time = Time(hdu.header['DATE-OBS']).gps
    pol = hdu.header['POLAR']

    fset = [file]

    for f in filelist:
        hdu = fits.open(f)[0]
        dt = np.abs(Time(hdu.header['DATE-OBS']).gps - time)
        newpol = hdu.header['POLAR']
        if (newpol != pol) and (dt < dtmax) :
            fset.append(f)

    #------------------------------------------------------------------------------
    complete, time = complete_set(fset)

    if complete:

        outfile = outdir + time.strftime('%Y%m%d_%H%M%S'+'_pBcom.fts')

        print(yellow+f"Creating pB composite file {outfile}"+cend)

        idlcommand = f"combine_stereo_pb,'{fset[0]}','{fset[1]}','{fset[2]}','{time.jd}','{outfile}'"
        subprocess.run([sswidl,"-e",idlcommand], env=os.environ)

        # remove complete set from file list
        for f in fset:
            try:
                filelist.remove(f)
            except ValueError:
                pass

