
import os
import time
from stereo_process_pB import process_files
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

"""
This function is for processing STEREO-A polarized brightness (pB) file in real-time "watch" mode.  The function runs continuously, monitoring a specified target directory for the appearance of a new file.  When a new fits file appears, the function will group this file with the previous two files in terms of the date of file creation.  Then it checks to see if these three files form a complete set.

A complete set consists of three observations with different polarization states (0, 120, and 240) all taken within 30 minutes of one another.  If a complete set is found, the three pB images are processed with the SolarSoft `secchi_prep` function and the images are combined to form a total brightness (tB) image.   This tB image is written as a fits file to a specified output directory.  The output file name reflects the date of the observation and includes the tag `pBcom` to represent a polarized brightness composite.

This function only works if the pB (seq) files arrive one at a time, with an intervening delay of at least 20 seconds.  If more than three files are added to the monitored directory simultaneously, then it will miss some files that should be processed.

If more than three files are added to the target directory at one time, then it is recommended to use the `process_dir.py` function instead of this one.

"""
#------------------------------------------------------------------------------
# define platform-specific parameters

# this is the directory to monitor for new files
#dir = '../data/seq'
targetdir = '../data/tmp/'

#output directory
outdir = '../data/pBcom/'

# location of sswidl executable
sswidl = '/usr/local/ssw/gen/setup/ssw_idl'

#------------------------------------------------------------------------------
red = '\033[91m'
yellow = '\033[93m'
cend = '\033[0m'

#------------------------------------------------------------------------------
# event handler

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        print(yellow+f"New image found: {event.src_path}"+cend)
        process_files(targetdir, outdir, event.src_path, sswidl)

#------------------------------------------------------------------------------
# main program that runs continually

if __name__ == "__main__":

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

    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, targetdir, recursive=False)
    observer.start()
    print("Monitoring for files....")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()