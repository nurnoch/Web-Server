# A simple WSGI server implementation
import socket
import StringIO
import sys
import time

class WSGIServer(object):
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5

    def __init__(self, server_address):
        # create a server socket
        self.server_socket = server_socket = socket.socket(self.address_family,
                self.socket_type
        )
        # allow to reuse the same address
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind to address
        server_socket.bind(server_address)
        # listening connections from client
        server_socket.listen(self.request_queue_size)
        # get server hostname and port
        host, port = self.server_socket.getsockname()[:2]
        self.server_name = host # return a fully qualified domain name
        self.server_port = port
        # return headers set by web applications
        self.headers_set = []

    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        server_socket = self.server_socket
        while True:
            self.client_connection, client_address = server_socket.accept()
            # handle this request
            self.handle_one_request()

    def handle_one_request(self):
        self.request_data = request_data = self.client_connection.recv(1024)
        print ''.join(['< {line}\n'.format(line = line) for line in request_data.splitlines()])

        # parse the first line of request to get http request infos
        self.parse_request(request_data)

        # construct environment dictionary using request data
        env = self.get_env()

        # call application and return a result will be HTTP response body
        result = self.application(env, self.start_response) # start_response is callable
        # send response to the client
        self.finish_response(result)

    def parse_request(self, text):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        (self.request_method, # GET
         self.path, # /hello
         self.request_version # HTTP 1.1
        ) = request_line.split()

    def get_env(self):
        env = {}
        # required WSGI variables
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = StringIO.StringIO(self.request_data)
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        # required CGI variables
        env['REQUEST_METHOD'] = self.request_method # GET
        env['PATH_INFO'] = self.path # /hello
        env['SERVER_NAME'] = self.server_name # localhost
        env['SERVER_PORT'] = str(self.server_port) # 8888
        return env

    def start_response(self, status, response_headers, exc_info = None):
        # add necessary server headers
        server_headers = [
                ('Date', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]
        # in WSGI specification this method must return a writable callable
        # to simplify we'll ignore it fow now
        # return self.finish_response

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status = status)
            for header in response_headers:
                response += '{0} : {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data
            print ''.join(
                ['> {line}\n'.format(line = line) for line in response.splitlines()])
            self.client_connection.sendall(response)
        finally:
            self.client_connection.close()

SERVER_ADDRESS = (HOST, PORT) = '', 8888

def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module: callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print "WSGIServer: Serving HTTP on port {port} ...\n".format(port = PORT)
    httpd.serve_forever()
