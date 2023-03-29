from threading import Thread
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter

import socket
import cv2
import pickle
#import struct
#import imutils
import timeit
import numpy as np

#sudo vim /sys/class/thermal/thermal_zone0/trip_point_4_temp
class Connection(Thread):
    def __init__(self, host_ip, port):
        Thread.__init__(self)
        self.host = (host_ip, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
        #self.interpreter = make_interpreter('../test_data/movenet_single_pose_lightning_ptq_edgetpu.tflite')
        self.interpreter = make_interpreter('../test_data/movenet_single_pose_thunder_ptq_edgetpu.tflite')
    
        self.interpreter.allocate_tensors()
        print("host name => ", self.host[0])
        print("host port => ", self.host[1])

    def __del__(self):
        self.client_socket.close()
        cv2.destroyAllWindows()

    

    def run(self):
        while 1:
            cap = cv2.VideoCapture(1)
            
            print("video start!!")
            while cap.isOpened():
                img, frame = cap.read()
                if not img:
                    print("no frame")
                    continue
                start_t = timeit.default_timer()
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


                # This resizes the RGB image
                resized_img = cv2.resize(frame_rgb, common.input_size(self.interpreter))
                # Send resized image to Coral
                common.set_input(self.interpreter, resized_img)

                # Do the job
                self.interpreter.invoke()

                # Get the pose
                self.pose = common.output_tensor(self.interpreter, 0).copy().reshape(17, 3)

                height, width, ch = frame.shape

                # Draw the pose onto the image using blue dots
                msg = []
                for i in range(0, 17):
                    msg.append(0)
                    msg.append(0)
                    if(self.pose[i][2]< 0.5):
                        continue
                    x = int(self.pose[i][1] * width)
                    y = int(self.pose[i][0] * height)
                    
                    msg[i*2] = x
                    msg[i*2 +1] = y
                    
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), 3)
                    #cv2.putText(frame, str(int(pose[i][2] * 100)), (x + 5, y + 5), cv2.FONT_ITALIC, 1, (0, 255, 0), 1)
                #print(msg)
                terminate_t = timeit.default_timer()
                time_diff = str(int(1/(terminate_t - start_t )))
                cv2.putText(frame, "FPS : " + time_diff, (80, 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                
                ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY),30])  # ret will returns whether connected or not, Encode image from image to Buffer code(like [123,123,432....])
                #print(type(pose))
                message = pickle.dumps([buffer, msg]) 

                self.client_socket.sendto(message, self.host)
                #cv2.imshow("Sending", frame)
                print(int(1./(terminate_t - start_t )))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    #connection = Connection("192.168.100.37", 10050)
    connection = Connection("192.168.100.105", 10050)
    connection.start()
