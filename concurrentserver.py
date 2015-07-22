##############################
# Concurrent server
# This server can handle multiple requests at the same time.
# Child process sleeps for 60 seconds after handling a request.
# Parent process accept a new connection and fork a child process to handle it.
##############################
import socket
import time
import os

REQUEST_QUEUE_SIZE = 5
SERVER_ADDRESS = (HOST, PORT) = '', 8888

def handle_one_request(client_connection):
    request_data = client_connection.recv(1024)
    print 'Child PID: {pid}. Parent PID {ppid}'.format(pid = os.getpid(), ppid = os.getppid())
    print request_data.decode()
    http_response = """
        HTTP/1.1 200 OK
        
        Hello, world!
    """
    client_connection.sendall(http_response)
    time.sleep(60) # block process for 60 seconds

def serve_forever():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(REQUEST_QUEUE_SIZE)
    print 'Serving HTTP on port {port} ...'.format(port = PORT)
    print 'Child PID: {pid}. Parent PID {ppid}'.format(pid = os.getpid(), ppid = os.getppid())

    while True:
        client_connection, client_address = server_socket.accept()
        pid = os.fork()
        if pid == 0:  # child
            print "I'm child"
            server_socket.close() # close child copy
            handle_one_request(client_connection)
            client_connection.close()
            os._exit(0)  # child exist
        else: # parent
            print "I'm parent"
            client_connection.close()  # close parent copy

if __name__ == '__main__':
    serve_forever()
