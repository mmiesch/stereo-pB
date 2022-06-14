"""
Script for processing polarized images from STEREO-A such that they can be used by the SWPC CME Analysis Tool (CAT)
"""


import numpy as numpy
import os
import subprocess

#------------------------------------------------------------------------------
# define file list

dir = 'data/seq/'

f = ['20220601_040835_n7c2A.fts', \
     '20220601_040905_n7c2A.fts', \
     '20220601_040935_n7c2A.fts'
]

#------------------------------------------------------------------------------

sswidl = "/usr/local/ssw/gen/setup/ssw_idl"

idlcommand = f"combine_stereo_pb,'{dir+f[0]}','{dir+f[1]}','{dir+f[2]}'"

subprocess.run([sswidl,"-e",idlcommand], env=os.environ)
