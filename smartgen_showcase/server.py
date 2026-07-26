"""
Development Server for SmartGen Showcase.
Handles live-reloading and serving the static site.
"""

import os
import http.server
import socketserver
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .core import SmartGenEngine

class ContentChangeHandler(FileSystemEventHandler):
    def __init__(self, config_path):
        self.config_path = config_path
        self.engine = SmartGenEngine(config_path=self.config_path)

    def on_any_event(self, event):
        if 'site' in event.src_path or event.is_directory:
            return
        print(f"\n[Live Reload] Change detected in: {event.src_path}")
        try:
            self.engine.process_content_files()
            print("✔ Rebuild successful! Refresh your browser.")
        except Exception as e:
            print(f"✖ Build failed: {e}")

class DevServer:
    def __init__(self, config_path='smartgen.yml', port=8000):
        self.config_path = config_path
        self.port = port
        self.site_dir = 'site'

    def run(self):
        print("Performing initial build...")
        engine = SmartGenEngine(self.config_path)
        engine.process_content_files()

        event_handler = ContentChangeHandler(self.config_path)
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=True)
        observer.start()

        if not os.path.exists(self.site_dir):
            os.makedirs(self.site_dir)
            
        os.chdir(self.site_dir)
        handler = http.server.SimpleHTTPRequestHandler
        socketserver.TCPServer.allow_reuse_address = True
        
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            print("============================================================")
            print(f"✔ Dev Server running at: http://localhost:{self.port}")
            print("============================================================")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nShutting down server...")
            finally:
                observer.stop()
                observer.join()