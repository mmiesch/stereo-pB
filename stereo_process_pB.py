"""
Script for processing polarized images from STEREO-A such that they can be used by the SWPC CME Analysis Tool (CAT)
"""


import numpy as np
import os
import subprocess

from astropy.io import fits
from astropy.time import Time

#------------------------------------------------------------------------------
# define file list

dir = 'data/seq/'

f = ['20220601_040835_n7c2A.fts', \
     '20220601_040905_n7c2A.fts', \
     '20220601_040935_n7c2A.fts'
]

#------------------------------------------------------------------------------
# read metadata

print(80*'-')

times = []
pol = []

for file in f:
    hdu = fits.open(dir+file)[0]
    times.append(Time(hdu.header['DATE']).gps)
    pol.append(hdu.header['POLAR'])

t = np.array(times)

time = Time(0.5*(np.min(t) + np.max(t)), format = 'gps')
time.format='iso'

print(f"time stamp = {time}")

for p in pol:
    print(f"pb file polarization {p}")


#------------------------------------------------------------------------------
# define an output file name based on the average time stamp

outfile = time.strftime('%Y%m%d_%H%M%S'+'_pBcom.fts')

print(f"outfile = {outfile}")

#------------------------------------------------------------------------------

sswidl = "/usr/local/ssw/gen/setup/ssw_idl"

idlcommand = f"combine_stereo_pb,'{dir+f[0]}','{dir+f[1]}','{dir+f[2]}'"

#subprocess.run([sswidl,"-e",idlcommand], env=os.environ)
