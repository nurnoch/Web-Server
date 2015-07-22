# Basic web server that handles one client request at a time
import socket

REQUEST_QUEUE_SIZE = 5
SERVER_ADDRESS = (HOST, PORT) = '', 8888

def handle_one_request(client_connection):
    request_data = client_connection.recv(1024)
    print request_data.decode()
    http_response = """
        HTTP/1.1 200 OK
        
        Hello, world!
    """
    client_connection.sendall(http_response)

def serve_forever():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(REQUEST_QUEUE_SIZE)
    print 'Serving HTTP on port {port} ...'.format(port = PORT)

    while True:
        client_connection, client_address = server_socket.accept()
        handle_one_request(client_connection)
        client_connection.close()

if __name__ == '__main__':
    serve_forever()
