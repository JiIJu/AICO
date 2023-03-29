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

    def get_frame(self):
        return self.data[0].tobytes()
 
    def get_ans(self):
        return self.ans

    def update(self):
        list_a = []
        
        model = load_model("C:\\Users\\multicampus\\Desktop\\gogo2\\S08P12C102\\web\\logintest\\record\\keras_model.h5", compile=False)
        class_names = open("C:\\Users\\multicampus\\Desktop\\gogo2\\S08P12C102\\web\\logintest\\record\\labels.txt", "r").readlines()


        self.good =0
        self.bad = 0
        cnt0,cnt1 =0,0
        while 1:
            
            try:
                packet = self.server_socket.recvfrom(100000000)
            except BlockingIOError:
                continue
            
            data = packet[0]
            self.data = pickle.loads(data)  # oriData[1] : 자세데이터
            dd = cv2.imdecode(self.data[0], cv2.IMREAD_COLOR)
            print(np.shape(dd))
              
            ##print(self.data[0].shape)
            #image = cv2.cvtColor(dd, cv2.COLOR_RGB2BGR)              
            image = cv2.resize(dd, (224, 224), interpolation=cv2.INTER_AREA)
            image = np.expand_dims(image, axis = 0)

            image = np.reshape(image, (1,224,224,3))
            
            prediction = model.predict(image)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            print(class_name[2:])
            list_a.append(int(class_name[2:]))
            

            

            i = list_a[-1]
            self.ans = i
            if i == 0 :
                cnt0 += 1
            elif i == 1:
                cnt1 += 1
                cnt0 = 0
                
            if cnt0 > 3 :
                if 10 <= cnt1 < 15:
                    self.bad += 1
                    cnt1= 0
                elif 15 <= cnt1 :
                    self.good += 1
                    cnt1 = 0
                elif 10 >= cnt1 :
                    cnt1 = 0
        
                    
            
        self.server_socket.close()