
import ssl, http.server, socketserver, os

AAB = r'C:\Users\DH\gay-app-list\android\app\build\outputs\bundle\release\app-release.aab'
certfile = r'C:\Users\DH\gay-app-list\server.crt'
keyfile = r'C:\Users\DH\gay-app-list\server.key'

class H(http.server.BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Request-Private-Network')

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_HEAD(self):
        self.send_response(200)
        self.send_cors_headers()
        self.send_header('Content-Type', 'application/octet-stream')
        self.send_header('Content-Length', str(os.path.getsize(AAB)))
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_cors_headers()
        self.send_header('Content-Type', 'application/octet-stream')
        self.send_header('Content-Length', str(os.path.getsize(AAB)))
        self.end_headers()
        with open(AAB, 'rb') as f: self.wfile.write(f.read())

    def log_message(self, *a): pass

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile, keyfile)
httpd = socketserver.TCPServer(('localhost', 8766), H)
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
print('HTTPS AAB server running on port 8766', flush=True)
httpd.serve_forever()
