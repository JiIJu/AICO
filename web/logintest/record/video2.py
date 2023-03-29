from django.utils import timezone
import threading
from datetime import datetime
import socket
import time
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
        threading.Thread(target=self.update3, args=()).start()

    def get_frame(self):
        return self.datas[0].tobytes()
 
    def get_ans(self):
        return self.ans

    def update3(self):
        while 1:
            try:
                packet = self.server_socket.recvfrom(100000000)
            except BlockingIOError:
                continue
            data = packet[0]
            self.datas = pickle.loads(data)

    def update(self):
        ## 스쿼트 : 0 : bad, 1 : good
        ## 프랭크 : 0 : good , 1 :bad
        
        self.list_a = []
        self.list_b = []
        
        model = load_model("C:\\Users\\multicampus\\Desktop\\gogo2\\S08P12C102\\web\\logintest\\record\\keras_model.h5", compile=False)
        model_2 = load_model("C:\\Users\\multicampus\\Desktop\\gogo2\\S08P12C102\\web\\logintest\\record\\keras_model_2.h5", compile=False)
        
        class_names = open("C:\\Users\\multicampus\\Desktop\\gogo2\\S08P12C102\\web\\logintest\\record\\labels.txt", "r").readlines()
        class_names_2 = open("C:\\Users\\multicampus\\Desktop\\gogo2\\S08P12C102\\web\\logintest\\record\\labels_2.txt", "r").readlines()
        


        self.goods =0
        self.bads = 0
            
        self.goodp = 0
        self.badp = 0
        self.cnt0,self.cnt1 =0,0
        self.cnt2_0, self.cnt2_1 = 0,0
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
            image = cv2.resize(dd, (224, 224), interpolation=cv2.INTER_AREA)
            image = np.expand_dims(image, axis = 0)

            image = np.reshape(image, (1,224,224,3))
            
            prediction = model.predict(image)
            prediction_2 = model_2.predict(image)
            
            index = np.argmax(prediction)
            index2 = np.argmax(prediction_2)

            class_name = class_names[index]
            class_name_2 = class_names_2[index2]
            #confidence_score = prediction[0][index]

            #print(class_name[2:])
            self.list_a.append(int(class_name[2:]))
            self.list_b.append(int(class_name_2[2:]))
            


            # i = list_a[-1]
            # list_a = []
            self.anss = int(class_name[2:])
            if self.anss == 0 :
                self.cnt0 += 1
            elif self.anss == 1:
                self.cnt1 += 1
                self.cnt0 = 0
                
            if self.cnt0 > 3 :
                if 10 <= self.cnt1 < 15:
                    self.bads += 1
                    self.cnt1= 0
                elif 15 <= self.cnt1 :
                    self.goods += 1
                    self.cnt1 = 0
                elif 10 >= self.cnt1 :
                    self.cnt1 = 0
                        
                        
            # j = list_b[-1] 
            # list_b = []
            self.ansp = int(class_name_2[2:])
            if self.ansp == 1 :
                self.cnt2_1 += 1
            elif self.ansp == 0:
                self.cnt2_0 += 1
                self.cnt2_0 = 0
                
            if self.cnt2_1 > 3 :
                if 10 <= self.cnt2_0 < 15:
                    self.badp += 1
                    self.cnt2_0= 0
                elif 15 <= self.cnt2_1 :
                    self.goodp += 1
                    self.cnt2_1 = 0
                elif 10 >= self.cnt2_1 :
                    self.cnt2_1 = 0
            
                    
            
        self.server_socket.close()