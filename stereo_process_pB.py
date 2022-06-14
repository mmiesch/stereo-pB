"""
Script for processing polarized images from STEREO-A such that they can be used by the SWPC CME Analysis Tool (CAT)
"""


import numpy as numpy
import os
import subprocess

#------------------------------------------------------------------------------
# define file list

pb_dir = 'data/seq/'

pb_files = ['20220601_040835_n7c2A.fts', \
            '20220601_040905_n7c2A.fts', \
            '20220601_040935_n7c2A.fts'
]

filelist = ""

for f in pb_files:
    filelist += pb_dir+f
    if f != pb_files[-1]:
        filelist += ','

#------------------------------------------------------------------------------

sswidl = "/usr/local/ssw/gen/setup/ssw_idl"

subprocess.run([sswidl,"-e",f"combine_stereo_pb,'{filelist}'"], env=os.environ)
