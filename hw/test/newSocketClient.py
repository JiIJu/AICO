from threading import Thread
from time import sleep
import socket

class Communication(Thread):
    def __init__(self, host):
        Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(host)
        
        # self.queue = queue
        self.daemon = True
        self._flag = False
        self.ID = "SINGSONGSANG"
        self.data = []

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

    def connect(self, host):
        try:
            self.client.connect(host)
        except:
            print(f"Client Connect Fail...")

    def run(self):
        while 1:
            self.send("INIT")
            data = self.client.recv(1024)
            
            if not data:
                sleep(0.5)
                continue

            data = data.decode()
            if data == "AICOISBEST":
                self.flag = True
                break

        print(f"{self.ID} 서버 접속이 완료 되었습니다!")
        # self.queue.put("OK")
        while self._flag:
            data = self.client.recv(1024)
            
            if not data:
                sleep(0.5)
                continue
            
            data = data.decode()
            self.data.append(data)
            print(f">> Received :d {data}")
        self.client.close()

if __name__ == "__main__" :
    communication = Communication(("172.26.6.71", 10000))
    communication.start()
    while 1:
        msg = str(input("메시지를 입력하세요!\n"))
        communication.send(msg)
