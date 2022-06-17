
import glob
import os

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
# define platform-specific parameters

# this is the directory to monitor for new files
#dir = '../data/seq'
targetdir = '../data/tmp/'

#output directory
outdir = '../data/pBcom/'

# location of sswidl executable
sswidl = "/usr/local/ssw/gen/setup/ssw_idl"

#------------------------------------------------------------------------------
# first get the file list of the target directory

files = list(filter(os.path.isfile, glob.glob(targetdir + "*.fts")))

if len(files) < 3:
    exit(0)

files.sort(key=lambda x: os.path.getmtime(x))

#------------------------------------------------------------------------------
# now loop over files, looking for a complete set

#for file in files:

#file = files[0]

#print(file)

complete, time = complete_set(files)

if complete:
    print(f"complete set {time}")
else:
    print("incomplete set")

