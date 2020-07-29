# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler

class proxy_request_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        req = self
        content_length = req.headers.get('Content-Length', 0)
        print('  Content-Length: {}'.format(content_length))
        self.send_response(200)
        self.send_header('Content-Length', 5)
        self.end_headers()
        self.wfile.write("body\n".encode('utf-8'))

    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET
    do_OPTIONS = do_GET

def run(handler_class=proxy_request_handler, server_class=HTTPServer, protocol="HTTP/1.1"):
    port = 8000
    server_address = ('',port)
    handler_class.protocol_version = protocol
    httpd = server_class(server_address, handler_class)
    print("Proxy server start port={}...".format(port))
    httpd.serve_forever()

run()
