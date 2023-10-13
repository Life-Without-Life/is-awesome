import socket
HOST = "127.0.0.1"
PORT = 65432
buffsize = 102
TCPSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
TCPSocket.connect((HOST,PORT))
TCPSocket.close()