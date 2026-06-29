#!/usr/bin/env python3
import http.server
import socketserver
import os

AAB_PATH = r"C:\Users\DH\gay-app-list\android\app\build\outputs\bundle\release\app-release.aab"
PORT = 8765

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/app-release.aab':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET')
            size = os.path.getsize(AAB_PATH)
            self.send_header('Content-Length', str(size))
            self.end_headers()
            with open(AAB_PATH, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(format % args)

with socketserver.TCPServer(("localhost", PORT), CORSHandler) as httpd:
    print(f"Serving AAB on port {PORT}")
    httpd.serve_forever()
