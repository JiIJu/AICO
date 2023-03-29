from threading import Thread
from time import sleep
import socket

class Communication(Thread):
    def __init__(self, host):
        Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(host)
        self.daemon = True
        self._flag = True
        self.ID = "AICOAICOAICOAICOAICO"
        self.data = ""

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, state):
        self._flag = state

    def __del__(self):
        self.send("DISCONNECToo")
        self.client.close()

    def send(self, msg):
        self.client.send(f"{self.ID} {msg}".encode())

    def run(self):
        while 1:
            self.send("INIT")
            data = self.client.recv(1024)
            
            if not data:
                print("no date")
                continue

            data = data.decode()
            if data == "AICOISBEST":
                break

        print(f"{self.ID} client next")
        while self._flag:
            data = self.client.recv(1024)
            
            if not data:
                print("no date")
                continue
            print(data.decode())
            

if __name__ == "__main__" :
    communication = Communication(("192.168.100.106", 10000))
    communication.start()

    sleep(1)
    while 1:
        msg = str(input("메시지를 입력하시오\n"))
        communication.send(msg)



