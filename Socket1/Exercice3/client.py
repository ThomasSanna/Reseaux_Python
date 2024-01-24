# Echo client program
import socket
from fonction import *
import random


HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    matrice = [['-','-','-'], 
               ['-','-','-'], 
               ['-','-','-']]
    
    num = random.randint(1, 2)
    numAdv = 3-num
    s.sendall(numAdv.to_bytes((numAdv.bit_length()+7)//8, 'big'))
    print("numéro", num)
    
    premierCommencer = False if num == 2 else True
        
    lancer(num, numAdv, matrice, premierCommencer, s)
        
print('Fin du jeu')