import os
import time
import subprocess
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class RestartHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = self.start_bot()

    def start_bot(self):
        return subprocess.Popen(["py", self.script])

    def on_any_event(self, event):
        if event.src_path.endswith("HISTORY.log"):
            return
        self.process.terminate()
        self.process = self.start_bot()

if __name__ == "__main__":
    path = "."
    event_handler = RestartHandler("main.py")  
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
