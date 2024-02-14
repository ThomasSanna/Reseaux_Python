# Echo server program
import socket
import random

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        n = random.randint(0, 10)
        while True:
            data = conn.recv(1024)
            dataN = int.from_bytes(data, "big")
            if not data:
                break
            
            if int.from_bytes(data, "big"):
                if  n == dataN:
                    message = 'Bravo'
                if n < dataN:
                    message = 'Plus Petit'
                if n > dataN:
                    message = 'Plus Grand'
                    
            conn.sendall(bytes(message, 'utf-8'))