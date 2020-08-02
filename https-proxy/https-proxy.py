# -*- coding: utf-8 -*-
#
# a simple http only proxy server.
#

from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection
from urllib.parse import urlparse

class ProxyRequestHandler(BaseHTTPRequestHandler):

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
                return (True,res_body)
            except Exception as e:
                print(e)
                self.send_error(502)
                return (False,'')
        else:
            return (False,'')

    def do_GET(self):
        req = self
        (flag,res_body) = self.get_remote_content()
        if flag:
            self.send_response(200)
            content_length = int(len(res_body))
            print('  length of remote contens: {}'.format(content_length))
            self.send_header('Content-Length', content_length)
            self.end_headers()
            self.wfile.write(res_body)
            self.wfile.flush()
        else:
            self.send_error(501,'Unsupported')

    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET
    do_OPTIONS = do_GET

def run(handler_class=ProxyRequestHandler, server_class=HTTPServer, protocol="HTTP/1.1"):
    port = 8080
    server_address = ('',port)
    handler_class.protocol_version = protocol
    httpd = server_class(server_address, handler_class)
    print("Proxy server start port={}...".format(port))
    httpd.serve_forever()

run()
