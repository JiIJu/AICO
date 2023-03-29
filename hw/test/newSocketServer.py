from threading import Thread
from time import sleep
import socket

class Client(Thread):
    def __init__(self, client, address):
        Thread.__init__(self)
        self.daemon = True
        self._flag = True
        self.client = client
        self.address = address
        self.clients = []
        self.ID = ""
        self.IDS = dict()

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, state):
        self._flag = state

    def send(self, msg):
        self.client.send(msg.encode())

    # def get_ID(self):
    #     id = (id for id in self.IDS if id["ID"] == self.ID)
    #     id = next(id, False)
    #     return id

    def get_IDS(self):
        return self.IDS

    def run(self):
        while self._flag:
            try:
                # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
                data = self.client.recv(1024)

                if not data:
                    sleep(0.5)
                    continue

                data = data.decode()
                ID = data.split(" ")[0]
                MSG = data.split(" ")[1]

                if MSG == "INIT":
                    self.ID = ID
                    self.IDS = {
                            "ID" : ID,
                            "IP" : self.address[0],
                            "MSG" : []
                        }
                    self.client.settimeout(1000)
                    print(f">> Connected : {[client.IDS for client in self.clients]}")
                    self.send("AICOISBEST")
                elif MSG == "DISCONNECToo":
                    break
                else:
                    self.IDS["MSG"].append(MSG)
                    print(f">> Received : {self.IDS}")

            except ConnectionResetError as e:
                print(f">> Disconnected : ('{self.address[0]}', {self.address[1]})")
                break
            except socket.timeout:
                print(f">> TimeOut : ('{self.address[0]}', {self.address[1]})")
                break

        self.clients.remove(self)
        print(f">> Connected : { [client.IDS for client in self.clients]}")
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
        self.about = []
        print("SERVER START!")

    # 현재 연결 되어있는 모든 클라이언트 리스트
    def get_clients(self):
        if len(self.about) >= len(self.clients):
            return self.about

        self.about = [client.IDS for client in self.clients]
        return self.about

    # 찾고 싶은 클라이언트, 시리얼 ID 입력해서 얻을 수 있음
    def get_client(self, who):
        id = (id for id in self.get_clients() if id["ID"] == who)
        id = next(id, False)
        return id
        
    def run(self):
        while 1:
            # client가 붙을 떄까지 여기서 대기
            client_socket, address = self.server_socket.accept()
            print(f">> Accepted : {address}")
            client_socket.setblocking(False)
            client_socket.settimeout(10)
            client = Client(client_socket, address)
            self.clients.append(client)
            client.clients = self.clients
            client.start()

if __name__ == "__main__" :
    communication = Communication(10000)
    communication.start()
    communication.join()