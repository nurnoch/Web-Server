import socket

HOST = 'localhost' # the remote host
PORT = 8888 # port used by server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to server
client_socket.connect((HOST, PORT))
# send something to the server
client_socket.sendall("Hello, world")
data = client_socket.recv(1024)
client_socket.close()
print 'Received', repr(data)

