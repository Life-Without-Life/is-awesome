import socket
from Crypto.Cipher import DES
HOST = "127.0.0.1"
PORT = 65432
buffsize = 1024
TCPSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
TCPSocket.connect((HOST,PORT))
data = '123456ABCD132536'
print(data)
key = 'AABB09182736CCDD'.encode('utf-8')
print(key)
cipher = DES.new(key[:8], DES.MODE_ECB)
ct = cipher.encrypt(data.encode('UTF-8'))
print(ct)
TCPSocket.sendall(key)
TCPSocket.sendall(ct)
pt = TCPSocket.recv(100000)
print(pt)
TCPSocket.close()