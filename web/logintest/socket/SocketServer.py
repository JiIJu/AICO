from threading import Thread
import socket

class Client(Thread):
    def __init__(self, client, address):
        Thread.__init__(self)
        self.daemon = True
        self._flag = True
        self.client = client
        self._IDS = []
        self.address = address
        self.ID = ""

    @property
    def IDS(self):
        return self._IDS

    @IDS.setter
    def IDS(self, id):
        self._IDS = id

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, state):
        self._flag = state

    def send(self, msg):
        self.client.send(msg.encode())

    def run(self):
        while self._flag:
            try:
                # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
                data = self.client.recv(1024)

                if not data:
                    continue

                data = data.decode()
                ID = data.split(" ")[0]
                MSG = data.split(" ")[1]

                if MSG == "INIT":
                    self.ID = ID
                    self.IDS.append({
                            "ID" : ID,
                            "IP" : self.address[0]
                        })
                    self.client.settimeout(1000)
                    print(f">> Connected : {self._IDS}")
                    self.send("AICOISBEST")
                elif MSG == "DISCONNECToo":
                    break
                else:
                    self.send("OK")

                print(f">> Received : ('{self.address[0]}', {ID}, {MSG})")

            except ConnectionResetError as e:
                print(f">> Disconnected : ('{self.address[0]}', {self.address[1]})")
                break
            except socket.timeout:
                print(f">> TimeOut : ('{self.address[0]}', {self.address[1]})")
                break
        id = (id for id in self._IDS if id["ID"] == self.ID)
        id = next(id, False)
        self.IDS.remove(id)
        print(f">> Connected : {self._IDS}")
        self.client.close()

class Communication(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)

        self.server_socket.bind((host_ip, port))
        self.server_socket.listen(5)

        self.daemon = True
        self.clients = [] #여기 5대 까지
        print("SERVER READY!")

    def run(self):
        while 1:
            # client가 붙을 떄까지 여기서 대기
            client_socket, address = self.server_socket.accept()
            print(f">> Accepted : {address}")
            client_socket.setblocking(False)
            client_socket.settimeout(10)
            client = Client(client_socket, address)
            client.IDS = self.clients
            client.start()

if __name__ == "__main__" :
    communication = Communication(10000)
    communication.start()
    communication.join()