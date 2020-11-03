import socket
from threading import Thread


def recvall():
    trigger = True
    data = b''
    data = client.recv(4096)
    while trigger == True:
        if b"EOFD" not in data:
            data += client.recv(4096)
        else:
            trigger = False
            data = data[:-4]
            return data


def client_accept():
    while True:
        data = recvall().decode(encoding="utf-8", errors="ignore")
        outData = input(data)
        client.sendall(outData.encode()+b"EOFD")
        if outData == "exit":
            s.close()
            print("Bağlantı Sonlandı")
            exit()
        data = recvall().decode(encoding="utf-8", errors="ignore")
        print(data)


host = ""
port = 3636

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

s.listen(1)
print("Dinliyorum..")

client, clientAdress = s.accept()
print("Gelen Bağlantı (", clientAdress, ")")

try:
    accept_thread = Thread(target=client_accept())
    accept_thread.start()
except:
    pass

s.close()
