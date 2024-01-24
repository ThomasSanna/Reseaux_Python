# Echo client program
import socket

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    dataMessage = ''
    while dataMessage != 'Bravo':
        
        message = int(input("Entier entre 0 et 10 : "))
        
        s.sendall(message.to_bytes(2, byteorder="big"))
        
        data = s.recv(1024)
        dataMessage = data.decode('utf-8')
        
        print(dataMessage)
        
print('Fin du jeu')