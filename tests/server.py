import http.server
import socketserver
json

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'1')

PORT = 8080

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Server listening on port", PORT)
    httpd.serve_forever()
