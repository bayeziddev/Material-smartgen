import http.server
import socketserver
import threading
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .core import Builder

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, builder):
        self.builder = builder

    def on_modified(self, event):
        if event.src_path.endswith(('.md', '.yml', '.html', '.css')):
            print(f"File {event.src_path} modified, rebuilding...")
            try:
                self.builder.build()
            except Exception as e:
                print(f"Build error: {e}")

class DevServer:
    def __init__(self, config_path, port=8000):
        self.config_path = config_path
        self.port = port
        self.site_dir = 'site'
        self.builder = Builder(config_path, self.site_dir)

    def run(self):
        # Initial build
        self.builder.build()

        # Start file watcher
        event_handler = ChangeHandler(self.builder)
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=True)
        observer.start()

        # Start HTTP server
        handler = http.server.SimpleHTTPRequestHandler
        
        # Change directory to site_dir for serving
        os.chdir(self.site_dir)
        
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            print(f"Serving at http://localhost:{self.port}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                observer.stop()
        
        observer.join()
