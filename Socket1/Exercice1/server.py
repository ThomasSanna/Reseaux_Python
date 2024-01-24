# Echo server program
import socket
from datetime import date
import calendar
import time

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            dataMessage = ' '.join(data.decode("utf-8").split()[1:])
            premierMot = data.split()[0].decode("utf-8")
            if premierMot == "LOWER":
                message = dataMessage.lower()
            elif premierMot == "UPPER":
                message = dataMessage.upper()
            elif premierMot == "DATENOW":
                GMT_now = time.gmtime()
                timestamp= calendar.timegm(GMT_now)
                message = "Timestamp actuel : ", timestamp+3600
            else:
                message = premierMot, dataMessage
            conn.sendall(bytes(message, 'utf-8'))