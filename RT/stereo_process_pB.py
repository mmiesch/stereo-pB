"""
Script for processing polarized images from STEREO-A such that they can be used by the SWPC CME Analysis Tool (CAT)
"""

import glob
import numpy as np
import os
import subprocess

from astropy.io import fits
from astropy.time import Time

#------------------------------------------------------------------------------
# define system-specific paramters

# input directory
dir = '../data/seq/'

# output directory
outdir = '../data/pBcom/'

# location of sswidl executable
sswidl = "/usr/local/ssw/gen/setup/ssw_idl"

#------------------------------------------------------------------------------
# retrieve the most recent three files in selected directory.

files = list(filter(os.path.isfile, glob.glob(dir + "*.fts")))
files.sort(key=lambda x: os.path.getmtime(x))

f = files[-3:]

for file in f:
    print(file)

#------------------------------------------------------------------------------
# read metadata

print(80*'-')

times = []
pol = []

for file in f:
    hdu = fits.open(file)[0]
    times.append(Time(hdu.header['DATE']).gps)
    pol.append(hdu.header['POLAR'])

#------------------------------------------------------------------------------
# define an output file name based on the average time stamp

t = np.array(times)

dt = np.max(t) - np.min(t)

time = Time(0.5*(np.min(t) + np.max(t)), format = 'gps')
time.format='iso'

print(f"time stamp, dt = {time} {dt}")

outfile = outdir + time.strftime('%Y%m%d_%H%M%S'+'_pBcom.fts')

print(f"outfile = {outfile}")

#------------------------------------------------------------------------------
# check for a matching set of polarizations
# and check that all the measurements are within 30 min of each other
# if a match, then run the procedure

set = [0.0, 120.0, 240.0]

# max allowable time difference, in seconds
dtmax = 1800.

for p in pol:
    print(f"pb file polarization {p}")

if all(x in pol for x in set) and dt < dtmax:
    print("complete set: creating pB composite file")
    idlcommand = f"combine_stereo_pb,'{f[0]}','{f[1]}','{f[2]}','{time.jd}','{outfile}'"
    subprocess.run([sswidl,"-e",idlcommand], env=os.environ)

else:
    print(f"incomplete set: exiting {pol} {dt/60}")

#------------------------------------------------------------------------------

