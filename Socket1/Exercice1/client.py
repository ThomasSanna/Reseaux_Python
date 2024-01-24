# Echo client program
import socket

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = str(input("Message : "))
    s.sendall(bytes(message, 'utf-8'))
    data = s.recv(1024)
    
print('Received', repr(data))