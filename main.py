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
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        #self._set_response()
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        if self.path=="/getlist":
            if "Cookie" in self.headers:
                c = cookies.SimpleCookie(self.headers["Cookie"])
                userhash = {'name': c['name'].value, 'UID': c['UID'].value}
                db = dbC()
                list_ = db.getlist(userhash)
                self.send_response(200)
                self.send_header('Access-Control-Allow-Credentials', 'true')
                self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                self.end_headers()
                self.wfile.write(list_.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Credentials', 'true')
                self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                self.end_headers()
                self.wfile.write("fail".encode('utf-8'))

    def do_POST(self):
        if self.path=="/login":
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
            #         str(self.path), str(self.headers), post_data.decode('utf-8'))
            user = eval(post_data) # <--- Converts the data to dict
            db = dbC()
            cookie = db.login(user)
            print(cookie)
            if(cookie):
                # The next line will do send_response(200) end_headers().
                # self._set_response()

                # Cus this is a cross domain setting cookies, so the following helps.
                # https://www.cnblogs.com/anai/p/4238777.html
                self.send_response(200)
                # cookies expires
                # http://michelanders.blogspot.com/2011/10/managing-session-id-with-cookies.html
                # http://b.leppoc.net/2010/02/12/simple-webserver-in-python/
                UID = "UID=" + cookie + ";Max-Age=604800"
                name = "name=" + user['name'] + ";Max-Age=604800"
                self.send_header('Access-Control-Allow-Credentials', 'true')
                self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                self.send_header('Set-Cookie', UID)
                self.send_header('Set-Cookie', name)
                self.end_headers()
                self.wfile.write("success".encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Credentials', 'true')
                self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                self.end_headers()
                self.wfile.write("fail".encode('utf-8'))
        elif self.path=="/dltext":
            if "Cookie" in self.headers:
                c = cookies.SimpleCookie(self.headers["Cookie"])
                content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
                post_data = self.rfile.read(content_length) # <--- Gets the data itself
                post_data_dict = eval(post_data) # <--- Converts the data to dict
                userhash = {'name': c['name'].value, 'UID': c['UID'].value, 'docHash':post_data_dict['docHash']}
                db = dbC()
                all_the_text = db.dltext(userhash)
                if all_the_text:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Credentials', 'true')
                    self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                    self.end_headers()
                    self.wfile.write(all_the_text.encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Credentials', 'true')
                    self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                    self.end_headers()
                    self.wfile.write("fail".encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Credentials', 'true')
                self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                self.end_headers()
                self.wfile.write("fail".encode('utf-8'))
        elif self.path=="/ultext":
            if "Cookie" in self.headers:
                c = cookies.SimpleCookie(self.headers["Cookie"])
                # print(c['UID'].value)
                content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
                post_data = self.rfile.read(content_length) # <--- Gets the data itself
                post_data_dict = eval(post_data) # <--- Converts the data to dict
                userhash = {'name': c['name'].value, 'UID': c['UID'].value}
                db = dbC()
                if db.ultext(userhash, post_data_dict):
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Credentials', 'true')
                    self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                    self.end_headers()
                    self.wfile.write("success".encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Credentials', 'true')
                    self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                    self.end_headers()
                    self.wfile.write("fail".encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Credentials', 'true')
                self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                self.end_headers()
                self.wfile.write("fail".encode('utf-8'))
        elif self.path=="/newtext":
            if "Cookie" in self.headers:
                c = cookies.SimpleCookie(self.headers["Cookie"])
                # print(c['UID'].value)
                content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
                post_data = self.rfile.read(content_length) # <--- Gets the data itself
                post_data_dict = eval(post_data) # <--- Converts the data to dict
                userhash = {'name': c['name'].value, 'UID': c['UID'].value}
                db = dbC()
                docHash = db.newtext(userhash, post_data_dict)
                if docHash:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Credentials', 'true')
                    self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                    self.end_headers()
                    self.wfile.write(docHash.encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Credentials', 'true')
                    self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                    self.end_headers()
                    self.wfile.write("fail".encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Credentials', 'true')
                self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                self.end_headers()
                self.wfile.write("fail".encode('utf-8'))
        elif self.path=="/delNotes":
            if "Cookie" in self.headers:
                c = cookies.SimpleCookie(self.headers["Cookie"])
                userhash = {'name': c['name'].value, 'UID': c['UID'].value}
                content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
                post_data = self.rfile.read(content_length) # <--- Gets the data itself
                post_data_dict = eval(post_data) # <--- Converts the data to dict
                db = dbC()
                if db.delNotes(userhash, post_data_dict['noteHash']):
                    db = dbC()
                    list_ = db.getlist(userhash)
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Credentials', 'true')
                    self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                    self.end_headers()
                    self.wfile.write(list_.encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Credentials', 'true')
                    self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                    self.end_headers()
                    self.wfile.write("fail".encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Credentials', 'true')
                self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                self.end_headers()
                self.wfile.write("fail".encode('utf-8'))
        elif self.path=="/reg":
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            user = eval(post_data) # <--- Converts the data to dict
            db = dbC()
            cookie = db.reg(user)
            print(cookie)
            if(cookie):
                # Cus this is a cross domain setting cookies, so the following helps.
                # https://www.cnblogs.com/anai/p/4238777.html
                self.send_response(200)
                # cookies expires
                # http://michelanders.blogspot.com/2011/10/managing-session-id-with-cookies.html
                # http://b.leppoc.net/2010/02/12/simple-webserver-in-python/
                UID = "UID=" + cookie + ";Max-Age=604800"
                name = "name=" + user['name'] + ";Max-Age=604800"
                self.send_header('Access-Control-Allow-Credentials', 'true')
                self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                self.send_header('Set-Cookie', UID)
                self.send_header('Set-Cookie', name)
                self.end_headers()
                self.wfile.write("success".encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Credentials', 'true')
                self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
                self.end_headers()
                self.wfile.write("fail".encode('utf-8'))
        else:
            pass    

    def do_OPTIONS(self):
        bool_ = self.path in ('*', '/login') or self.path in ('*', '/dltext')\
        or self.path in ('*', '/ultext') or self.path in ('*', '/newtext')\
        or self.path in ('*', '/delNotes') or self.path in ('*', '/reg')
        if bool_:
            self.send_response(200)
            self.send_header('Allow', 'GET, OPTIONS, POST')
            # https://stackoverflow.com/questions/19743396/cors-cannot-use-wildcard-in-access-control-allow-origin-when-credentials-flag-i
            self.send_header('Access-Control-Allow-Credentials', 'true')
            self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1')
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
