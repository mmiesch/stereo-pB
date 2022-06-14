"""
Script for processing polarized images from STEREO-A such that they can be used by the SWPC CME Analysis Tool (CAT)
"""


import numpy as numpy
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
    times.append(Time(hdu.header['DATE']))
    pol.append(hdu.header['POLAR'])


for t in times:
    print(t)

for p in pol:
    print(f"pb file polarization {p}")



#------------------------------------------------------------------------------
# define a representative time and output file name


#------------------------------------------------------------------------------

sswidl = "/usr/local/ssw/gen/setup/ssw_idl"

idlcommand = f"combine_stereo_pb,'{dir+f[0]}','{dir+f[1]}','{dir+f[2]}'"

#subprocess.run([sswidl,"-e",idlcommand], env=os.environ)
