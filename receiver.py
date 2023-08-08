import socket
from Crypto.Cipher import DES
HOST = "127.0.0.1"
PORT = 65432
buffsize = 1024
TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPSocket.bind((HOST, PORT))
TCPSocket.listen()
print("Server open for connection")
conn, addr = TCPSocket.accept()
print("Client Address: ", addr)
data = conn.recv(buffsize)
key = data
data = conn.recv(buffsize)
ct = data
print(key)
cipher = DES.new(key[:8], DES.MODE_ECB)
print(ct)
pt = cipher.decrypt(ct)
print(pt)
conn.sendall(pt)
conn.close()
