# -*- coding: utf-8 -*-
#
# a simple http/https proxy server.
#

import socket
import select
import sys
import ssl
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection
from urllib.parse import urlparse
from socketserver import ThreadingMixIn


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    address_family = socket.AF_INET6
    daemon_threads = True

    def handle_error(self, request, client_address):
        cls, e = sys.exc_info()[:2]
        if cls is socket.error or cls is ssl.SSLError:
            pass
        else:
            return HTTPServer.handle_error(self, request, client_address)

class ProxyRequestHandler(BaseHTTPRequestHandler):
    timeout = 10
    send_delay = 1/10.0
    blocksize = 1024 * 100

    def get_remote_content(self):
        req = self
        content_length = req.headers.get('Content-Length', 0)

        path = req.path
        host = req.headers['Host']
        obj  = urlparse(path)

        if obj.scheme == 'http':
            try:
                conn = HTTPConnection(host,obj.port)
                req_body = self.rfile.read(content_length) if content_length else None
                #conn.set_debuglevel(1)
                conn.request('GET', path, req_body, dict(req.headers))
                res = conn.getresponse()
                res_body = res.read()
                res_location = res.headers.get('Location')
                res_code = res.code
                return (True,res_code,res_location,res_body)
            except Exception as e:
                print(e)
                self.send_error(502)
                return (False,502,'','')
        else:
            return (False,502,'','')

    def do_GET(self):
        req = self
        (flag,res_code,res_location,res_body) = self.get_remote_content()
        if flag:
            self.send_response(res_code)
            content_length = int(len(res_body))
            print('  length of remote content: {}'.format(content_length))
            self.send_header('Content-Length', content_length)
            if 301 == res_code:
                self.send_header('Location', res_location)
            self.end_headers()
            self.wfile.write(res_body)
            self.wfile.flush()
        else:
            self.send_error(501,'Unsupported')

    def do_CONNECT(self):
        address = self.path.split(':',1)
        print(address)
        print('  CONNECT to remote (host,port,timeout): ({},{},{})'.format(address[0],address[1],self.timeout))
        try:
            s = socket.create_connection(address, timeout = self.timeout)
        except Exception as e:
            self.send_error(502)
            return
        self.send_response(200, 'Connection Established')
        self.end_headers()

        conns = [self.connection, s]
        self.close_connection = 0
        while not self.close_connection:
            rlist,wlist,xlist = select.select(conns, [], conns, self.timeout)
            if xlist or not rlist:
                break
            for r in rlist:
                other = conns[1] if r is conns[0] else conns[0]
                data = r.recv(self.blocksize)
                if not data:
                    self.close_connection = 1
                    break
                other.sendall(data)
                time.sleep(self.send_delay)

    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET
    do_OPTIONS = do_GET

def run(handler_class=ProxyRequestHandler, server_class=ThreadingHTTPServer, protocol="HTTP/1.1"):
    port = 8080
    server_address = ('',port)
    handler_class.protocol_version = protocol
    httpd = server_class(server_address, handler_class)
    print("Proxy server start port={}...".format(port))
    httpd.serve_forever()

run()
