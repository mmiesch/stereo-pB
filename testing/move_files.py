"""
move files from one directory to another
with a delay
"""

import glob
import os
import time
import shutil

source_dir = '../data/seq/'
target_dir = '../data/tmp/'

files = list(filter(os.path.isfile, glob.glob(source_dir + "*.fts")))
files.sort(key=lambda x: os.path.getmtime(x))

for f in files:
    file = f.split('/')[-1]
    print(file)
    shutil.move(source_dir+file, target_dir + file)
    time.sleep(20)

