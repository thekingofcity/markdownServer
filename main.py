#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7
"""
from http import cookies
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import sqlite3
from dbC import dbC

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #         str(self.path), str(self.headers), post_data.decode('utf-8'))
        post_data_dict = eval(post_data) # <--- Converts the data to dict
        print(post_data_dict['name'])
        print(post_data_dict['password'])
        user = {'name':post_data_dict['name'], 'password':post_data_dict['password']}
        db = dbC()
        cookie = db.login(user)
        print(cookie)
        if(cookie):
            # The next line will do send_response(200) end_headers().
            # self._set_response()

            # Cus this is a cross domain setting cookies, so the following helps.
            # https://www.cnblogs.com/anai/p/4238777.html
            self.send_response(200)
            UID = "UID=" + cookie
            name = "name=" + post_data_dict['name']
            self.send_header('Access-Control-Allow-Credentials', 'true')
            self.send_header('Access-Control-Allow-Origin', 'https://127.0.0.1')
            self.send_header('Set-Cookie', UID)
            self.send_header('Set-Cookie', name)
            self.end_headers()
            self.wfile.write("success".format(self.path).encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', 'https://127.0.0.1')
            self.end_headers()
            self.end_headers()
            self.wfile.write("fail".format(self.path).encode('utf-8'))
                

    def do_OPTIONS(self):
        if self.path in ('*', '/login'):
            self.send_response(200)
            self.send_header('Allow', 'GET, OPTIONS, POST')
            # https://stackoverflow.com/questions/19743396/cors-cannot-use-wildcard-in-access-control-allow-origin-when-credentials-flag-i
            self.send_header('Access-Control-Allow-Credentials', 'true')
            self.send_header('Access-Control-Allow-Origin', 'https://127.0.0.1')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Access-Control-Allow-Origin, Authorization, X-Requested-With')
            self.send_header('Content-Type', 'application/json')
        else:
            self.send_response(404)
        self.send_header('Content-Length', '0')
        self.end_headers()

def run(server_class=HTTPServer, handler_class=S, port=5000):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
