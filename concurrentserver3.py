##############################
# Concurrent server 3
# To set up a SIGCHILD event handler and wait for a terminated child in the event handler
#  When a child process exits, the kernel sends a SIGCHLD signal. 
# The parent process can set up a signal handler to be asynchronously notified 
# of that SIGCHLD event and then it can wait for the child to collect its termination status, 
# thus preventing the zombie process from being left around.
##############################
import socket
import time
import os
import signal
import errno

REQUEST_QUEUE_SIZE = 1024
SERVER_ADDRESS = (HOST, PORT) = '', 8888


def grim_reaper(signum, frame):
    # Wait for completion of a child process, 
    # and return a tuple containing its pid and exit status indication
    pid, status = os.wait()
    print 'Child {pid} terminated with status {status}'.format(pid = pid, status = status)

def handle_one_request(client_connection):
    request_data = client_connection.recv(1024)
    print 'Child PID: {pid}. Parent PID {ppid}'.format(pid = os.getpid(), ppid = os.getppid())
    print request_data.decode()
    http_response = """
        HTTP/1.1 200 OK
        
        Hello, world!
    """
    client_connection.sendall(http_response)
    time.sleep(3)

def serve_forever():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(REQUEST_QUEUE_SIZE)
    print 'Serving HTTP on port {port} ...'.format(port = PORT)

    # Set the handler for signal signalnum to the function handler. 
    signal.signal(signal.SIGCHLD, grim_reaper)

    while True:
        try:
            client_connection, client_address = server_socket.accept()
        except IOError as e:
            code, msg = e.args
            # restart 'accept' if it was interrupted
            if code == errno.EINTR:
                continue
            else:
                raise

        pid = os.fork()
        if pid == 0:  # child
            server_socket.close() # close child copy
            handle_one_request(client_connection)
            client_connection.close()
            os._exit(0)  # child exist
        else: # parent
            client_connection.close()  # close parent copy

if __name__ == '__main__':
    serve_forever()
