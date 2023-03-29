import socket
import cv2
import pickle
import struct
import imutils

server_socekt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print("host ip => ", host_ip)

port = 10050
socket_address = (host_ip, port)
print("socekt created")

server_socekt.bind(socket_address)
print("socket bind complete")

server_socekt.listen(5)
print("socket now listening")

while 1:
    client_socket, addr = server_socekt.accept()
    print("connection from => ", addr)
    if client_socket :
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            img, frame = cap.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            cv2.imshow("Sending", frame)
            if cv2.waitKey(10) == 13:
                client_socket.close()