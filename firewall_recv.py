import socket
HOST = "127.0.0.1"
PORT = 65432
buffsize = 1024
TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPSocket.bind((HOST, PORT))
TCPSocket.listen()
set_ip = ['127.0.0.1']
print("Server open for connection")
conn, addr = TCPSocket.accept()
if addr[0] not in set_ip:
    print("Address out of range")
else:
    print("Client Address: ", addr)
conn.close()
TCPSocket.close()