
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

"""
Example of watchdog module in python
"""

# this is the directory to monitor for new files
dir = '../data/tmp'


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        print("New image found: ", event.src_path)


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