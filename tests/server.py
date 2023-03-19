import http.server
import socketserver
import json
import asyncio
import aiohttp
import tracemalloc


class MyHandler(http.server.BaseHTTPRequestHandler):
    # def do_GET(self):
    #     response_body = "1"
    #     response = {"response": response_body}
    #     response_json = json.dumps(response)

    #     self.send_response(200)
    #     self.send_header('Content-type', 'application/json')
    #     self.end_headers()
    #     self.wfile.write(response_json.encode())


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        message = post_data.decode('utf-8')

        response_body = "1"
        response = {"response": response_body}
        response_json = json.dumps(response)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_json.encode())


PORT = 8080
HOST = '0.0.0.0'
async def main(loop):
    server = socketserver.TCPServer((HOST, PORT), MyHandler)
    print(f"Server listening on {HOST}:{PORT}")
    await loop.run_in_executor(None, server.serve_forever)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
