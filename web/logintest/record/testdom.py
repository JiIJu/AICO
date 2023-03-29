# opencv 웹캠


from django.utils import timezone
import threading
from datetime import datetime
import cv2
# from record.models import Image
import socket

import pickle
from sklearn.metrics import mean_absolute_error
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from . import views
from django.shortcuts import redirect,render

class VideoCamera(object):
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        #host_ip = "192.168.100.246"
        print(f"name : {host_name} ip : {host_ip}")
        port = 10050
        self.server_socket.bind((host_ip, port))
        print("socket bind complete")
        self.server_socket.setblocking(False)
        threading.Thread(target=self.update, args=()).start()
    

    def get_frame(self):
        return self.data[0].tobytes()

    def get_ans(self):
        return self.ans

    def update(self):
        move = pd.read_excel(
            'C:\\Users\\multicampus\\Desktop\\gogo2\\S08P12C102\\web\\logintest\\record\\real_test_Ver2.xlsx')

        cell = move.iloc[1:3332, 0:34]
        label = move.iloc[1:3332, 34]
        kn = KNeighborsClassifier()

        kn.n_neighbors = 5
        kn.fit(cell, label)

        zero = 1
        first = 0
        second = 0

        cycle01 = 0
        cycle10 = 0
        cycle02 = 0
        
        self.good = 0
        self.bad = 0
        self.a = [0]

        while 1:
            try:
                packet = self.server_socket.recvfrom(100000000)
            except BlockingIOError:
                continue
            print('되냐?')
            data = packet[0]
            self.data = pickle.loads(data)  # oriData[1] : 자세데이터
            # print(self.data[1]) frame
            # #self.ans = kn.predict([self.data[1]])
            # self.a.append(self.ans[0])
            # if zero == 1 and first == 0 and self.ans == 1 :  
            #     zero = 0
            #     first = 1
            #     cycle01 += 1
                
            # elif zero == 0 and first == 1 and self.ans == 0 :
            #     zero = 1
            #     first = 0
            #     cycle10 += 1
                
            # elif zero == 1 and second == 0 and self.ans == 2 :
            #     zero = 0
            #     second = 1
            #     cycle02 += 1
                
            # elif zero == 1 and second == 1 and self.ans == 0 :
            #     zero = 1
            #     second= 0
            #     cycle02 = 0

            # elif zero == 0 and second == 1 and self.ans == 2 and cycle02 == 1:
            #     second = 0
            #     cycle02 = 0
            #     zero = 1
            
            
            # if cycle02 == 1 :
            #     if cycle01 == 2 and cycle10 == 2 :
            #         self.good += 1
            #         cycle01 = 0
            #         cycle10 = 0
            #         cycle02 = 0
            #         zero = 1
            #     if cycle01 == 0 or cycle10 == 0 :
            #         self.bad += 1
            #         cycle01 = 0
            #         cycle10 = 0
            #         cycle02 = 0
            #         zero = 1

            # elif cycle02 == 0 :
            #     second = 0
                
            #     if cycle01 >= 4 or cycle10 >= 4 :
            #         self.bad += 1
            #         cycle01 = 0
            #         cycle10 = 0
            #         cycle02 = 0
                


        self.server_socket.close()