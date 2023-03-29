from django.utils import timezone
import threading
from datetime import datetime
import socket

import pickle
import pandas as pd
from keras.models import load_model
import cv2  
import numpy as np

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
        #threading.Thread(target=self.update2, args=()).start()
        threading.Thread(target=self.update3, args=()).start()

    def get_frame(self):
        return self.datas[0].tobytes()
 
    def get_ans(self):
        return self.ans

    # 팔굽
    # def update2(self):
    #     self.list_p = []
    #     model_2 = load_model("C:\\Users\\multicampus\\Desktop\\gogo2\\S08P12C102\\web\\logintest\\record\\keras_model_2.h5", compile=False)
    #     class_names_2 = open("C:\\Users\\multicampus\\Desktop\\gogo2\\S08P12C102\\web\\logintest\\record\\labels_2.txt", "r").readlines()
    
    #     print('여기냐?')
    #     self.cnt2_0 = 0
    #     self.cnt2_1 = 0                        
    #     self.goodp = 0
    #     self.badp = 0
    #     while 1:
            
    #         try:
    #             packet = self.server_socket.recvfrom(100000000)
    #         except BlockingIOError:
    #             continue
            
    #         data = packet[0]
    #         self.data = pickle.loads(data)  # oriData[1] : 자세데이터
    #         dd = cv2.imdecode(self.data[0], cv2.IMREAD_COLOR)
    #         print(np.shape(dd))
              
    #         #image = cv2.cvtColor(dd, cv2.COLOR_RGB2BGR)              
    #         image = cv2.resize(dd, (480, 640), interpolation=cv2.INTER_AREA)
    #         image = np.expand_dims(image, axis = 0)

    #         image = np.reshape(image, (1,480,640,3))
            
    #         prediction_2 = model_2.predict(image)
            
    #         index = np.argmax(prediction_2)
    #         class_name_2 = class_names_2[index]
    #         #confidence_score = prediction[0][index]

    #         #print(class_name[2:])
    #         self.list_p.append(int(class_name_2[2:]))
            
                        
    #         self.ansp = int(class_name_2[2:])
 
    #         j = self.ansp
    #         if j == 0 :
    #             self.cnt2_0 += 1
    #         elif j == 1:
    #             self.cnt2_1 += 1
    #             self.cnt2_0 = 0
    #         if self.cnt2_0 > 3 :
    #             if self.cnt2_1 < 10:
    #                 self.cnt2_1 = 0
    #             elif 10 <= self.cnt2_1 < 15:
    #                 self.badp += 1
    #                 self.cnt2_1= 0
    #             elif 15 <= self.cnt2_1 :
    #                 self.goodp += 1
    #                 self.cnt2_1 = 0


    def update3(self):
        while 1:
            try:
                packet = self.server_socket.recvfrom(100000000)
            except BlockingIOError:
                continue
            data = packet[0]
            self.datas = pickle.loads(data)


     # 스쿼트   
    def update(self):
        ## 스쿼트 : 0 : bad, 1 : good
        ## 프랭크 : 0 : good , 1 :bad
        
        self.list_s = []
        model = load_model("C:\\Users\\multicampus\\Desktop\\gogo2\\S08P12C102\\web\\logintest\\record\\fuck_cnn.h5", compile=False)
        class_names = open("C:\\Users\\multicampus\\Desktop\\gogo2\\S08P12C102\\web\\logintest\\record\\labels.txt", "r").readlines()
        
        self.cnt0 = 0
        self.cnt1 = 0
        self.goods = 0
        self.bads = 0
        while 1:
            
            try:
                packet = self.server_socket.recvfrom(100000000)
            except BlockingIOError:
                continue
            
            data = packet[0]
            self.data = pickle.loads(data)  # oriData[1] : 자세데이터
            dd = cv2.imdecode(self.data[0], cv2.IMREAD_COLOR)
            print(np.shape(dd))
              
            #image = cv2.cvtColor(dd, cv2.COLOR_RGB2BGR)              
            image = cv2.resize(dd, (480, 640), interpolation=cv2.INTER_AREA)
            image = np.expand_dims(image, axis = 0)
            image = (image / 127.5) - 1
            
            prediction = model.predict(image)
            
            index = np.argmax(prediction)
            class_name = class_names[index]
            #confidence_score = prediction[0][index]

            #print(class_name[2:])
            self.list_s.append(int(class_name[2:]))
            
            self.anss = int(class_name[2:])

            i = self.anss

            if i == 0 :
                self.cnt0 += 1
            elif i == 1:
                self.cnt1 += 1
                self.cnt0 = 0
        

            if self.cnt0 > 3 :
                if 2 <= self.cnt1 < 5:
                    self.bads += 1
                    self.cnt1= 0
                elif 5 <= self.cnt1 :
                    self.goods += 1
                    self.cnt1 = 0
                elif 1 >= self.cnt1 :
                    self.cnt1 = 0

   
            
        self.server_socket.close()