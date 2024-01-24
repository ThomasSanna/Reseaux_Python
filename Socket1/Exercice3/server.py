# Echo server program
import socket
from fonction import *

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    
    matrice = [['-','-','-'], 
               ['-','-','-'], 
               ['-','-','-']]
    
    # numeroJoueurServ = random.randint(1, 2)
    # numeroJoueurClient = 1 if numeroJoueurServ == 2 else 2
    
    num = conn.recv(1024)
    num = int.from_bytes(num, byteorder='little')
    numAdv = 3-int(num)
    print("numéro", num)
    
    premierCommencer = False if num == 2 else True
    
    
    with conn:
        print('Connected by', addr)

        lancer(num, numAdv, matrice, premierCommencer, conn)
            
print('Fin du jeu')
