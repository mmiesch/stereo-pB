"""
Script for processing polarized images from STEREO-A such that they can be used by the SWPC CME Analysis Tool (CAT)
"""


import numpy as numpy
import os
import subprocess

message = "hello"

sswidl = "/usr/local/ssw/gen/setup/ssw_idl"

subprocess.run([sswidl,"-e",f'print,\"{message}\"'], env=os.environ)
