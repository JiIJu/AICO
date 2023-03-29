from threading import Thread
from time import sleep
import socket

class Communication(Thread):
    def __init__(self, host, event):
        Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(host)
        
        self.event = event
        self.daemon = True
        self.flag = False
        self.ID = "AICOAICOAICOAICOAICO"


    def __del__(self):
        self.send("DISCONNECToo")
        self.client.close()

    def send(self, msg):
        self.client.send(f"{self.ID} {msg}".encode())

    def connect(self, host):
        try:
            self.client.connect(host)
        except:
            print(f"Client >> Connect Fail...")

    def run(self):
        while 1:
            sleep(1)
            self.send("INIT")
            data = self.client.recv(1024)
            
            if not data:
                continue

            data = data.decode()
            if data == "AICOISBEST":
                self.flag = True
                break

        print(f"Client >> {self.ID} Connected!")
        self.event.set()

        while self.flag:
            sleep(3)
            data = self.client.recv(1024)
            
            if not data:
                continue
            
            data = data.decode()
            print(f"Client >> Received : {data}")
        self.client.close()

if __name__ == "__main__" :
    communication = Communication(("192.168.100.37", 10000))
    communication.start()
