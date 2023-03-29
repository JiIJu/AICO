import socket
import cv2
import pickle
import struct
import imutils

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
#host_ip = "192.168.100.105"
port = 10050

print("host name => ", host_name)
print("host ip => ", host_ip)
print("host port => ", port)

print("socekt created")

server_socket.bind((host_ip, port))
print("socket bind complete")
server_socket.setblocking(False)



while 1:
    try:
        packet = server_socket.recvfrom(100000000)
    except BlockingIOError:
        continue

    data = packet[0]
    #print(type(data)) #<class 'bytes'>
    data = pickle.loads(data)
    
    #print(type(data)) #<class 'numpy.ndarray'>
    data = cv2.imdecode(data, cv2.IMREAD_COLOR) 
    cv2.imshow("RECEIVING...", data)
    if cv2.waitKey(1) == 13:
        break
server_socket.close()

