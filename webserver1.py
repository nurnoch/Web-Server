import socket

HOST, PORT = '', 8888

# create an INET, STREAMing socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# reuse socket in TIME_WAIT state
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to any address and port 8888
server_socket.bind((HOST, PORT))
# queue up max 5 connect requests
server_socket.listen(5)
print "Serving HTTP on port %s ... " % PORT

# enter the main loop of the web server
while True:
    # accept connections from outside, return a pair(conn, address)
    client_connection, client_address = server_socket.accept()
    # receive data from the socket
    request = client_connection.recv(1024)
    print request

    http_response = """HTTP/1.1 200 OK

        Hello, world!
    """
    
    # send all data from string
    client_connection.sendall(http_response)
    client_connection.close()
