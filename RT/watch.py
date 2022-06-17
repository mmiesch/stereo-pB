
import time
from stereo_process_pB import process_files
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

"""
Example of watchdog module in python
"""
#------------------------------------------------------------------------------
# define platform-specific parameters

# this is the directory to monitor for new files
#dir = '../data/seq'
dir = '../data/tmp/'

#output directory
outdir = '../data/pBcom/'

# location of sswidl executable
sswidl = "/usr/local/ssw/gen/setup/ssw_idl"

#------------------------------------------------------------------------------
# event handler

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        print("New image found: ", event.src_path)
        process_files(dir, outdir, sswidl)

#------------------------------------------------------------------------------
# main program that runs continually

if __name__ == "__main__":
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, dir, recursive=False)
    observer.start()
    print("Monitoring for files....")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()