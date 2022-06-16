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
# retrieve the most recent three files in a directory.

dir = 'data/seq/'

files = list(filter(os.path.isfile, glob.glob(dir + "*")))
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
# check for a matching set of polarizations

for p in pol:
    print(f"pb file polarization {p} {type(p)}")

set = [0.0, 120.0, 240.0]

if all(x in pol for x in set):
    print("complete set")
else:
    print("incomplete set")

#------------------------------------------------------------------------------
# define an output file name based on the average time stamp

t = np.array(times)

time = Time(0.5*(np.min(t) + np.max(t)), format = 'gps')
time.format='iso'

print(f"time stamp = {time}")

outfile = time.strftime('%Y%m%d_%H%M%S'+'_pBcom.fts')

print(f"outfile = {outfile}")

#------------------------------------------------------------------------------

sswidl = "/usr/local/ssw/gen/setup/ssw_idl"

idlcommand = f"combine_stereo_pb,'{dir+f[0]}','{dir+f[1]}','{dir+f[2]}'"

#subprocess.run([sswidl,"-e",idlcommand], env=os.environ)
