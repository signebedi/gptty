import http.server
import socketserver
import json
import asyncio
import aiohttp
import tracemalloc
import time
import random

# List of Shakespeare quotes to use as dummy responses
shakespeare_quotes = [
    "All the world's a stage, and all the men and women merely players.",
    "Once more unto the breach, dear friends, once more.",
    "Uneasy lies the head that wears a crown.",
    "All the perfumes of Arabia will not sweeten this little hand.",
    "The first thing we do, let's kill all the lawyers."
]

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

        response_body = random.choice(shakespeare_quotes)
        response = {"response": response_body}
        response_json = json.dumps(response)

        # Wait a random amount of time between 1 and 10 seconds
        # time.sleep(random.uniform(1, 10))

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
