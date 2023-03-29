from threading import Thread
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter
from time import sleep
import socket
import cv2
import pickle
import timeit


class Video(Thread):
    def __init__(self, host, event):
        Thread.__init__(self)
        
        self.host = host
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
        self.event = event
        self.daemon = True
        self.flag = False
        self.msg = [0] * 34
        self.modes = []
        self.state = -1
        #self.interpreter = make_interpreter('../test_data/movenet_single_pose_lightning_ptq_edgetpu.tflite')
        self.interpreter = make_interpreter('../test_data/movenet_single_pose_thunder_ptq_edgetpu.tflite')
        self.interpreter.allocate_tensors()

        print("host name => ", self.host[0])
        print("host port => ", self.host[1])

    def __del__(self):
        self.client_socket.close()

    def stop_video(self):
        self.flag = False

    def run_0(self, cap):
        # msg = [0] * 34
        print("run_0 >> START")
        while self.flag:
            img, frame = cap.read()

            if not img:
                print("run_0 >> No Frame")
                return

            start_t = timeit.default_timer()

            # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # resized_img = cv2.resize(frame_rgb, common.input_size(self.interpreter))
            # common.set_input(self.interpreter, resized_img)
            # self.interpreter.invoke()
            # pose = common.output_tensor(self.interpreter, 0).copy().reshape(17, 3)

            # height, width, ch = frame.shape

            # for i in range(0, 17):
            #     msg[i*2] = 0.0
            #     msg[i*2 +1] = 0.0

            #     if(pose[i][2]< 0.5):
            #         continue
                    
            #     x = int(pose[i][1] * width)
            #     y = int(pose[i][0] * height)
                
            #     msg[i*2] = pose[i][1]    # x
            #     msg[i*2 +1] = pose[i][0] # y
                
            #     cv2.circle(frame, (x, y), 5, (0, 255, 0), 3)

            terminate_t = timeit.default_timer()
            time_diff = str(int(1/(terminate_t - start_t )))
            
            # cv2.putText(frame, "FPS : " + time_diff, (80, 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            
            ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY),30])
            message = pickle.dumps([buffer, time_diff])
            self.client_socket.sendto(message, self.host)

            #print(f"run_0 : {time_diff}")


    def run_1(self, cap):
        # msg = [0] * 34
        print("run_1 >> START")
        while self.flag:
            img, frame = cap.read()

            if not img:
                print("run_1 >> no frame")
                return

            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            start_t = timeit.default_timer()

            # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # resized_img = cv2.resize(frame_rgb, common.input_size(self.interpreter))
            # common.set_input(self.interpreter, resized_img)
            # self.interpreter.invoke()
            # pose = common.output_tensor(self.interpreter, 0).copy().reshape(17, 3)

            # height, width, ch = frame.shape

            # for i in range(0, 17):
            #     msg[i*2] = 0.0
            #     msg[i*2 +1] = 0.0

            #     if(pose[i][2]< 0.5):
            #         continue
                    
            #     x = int(pose[i][1] * width)
            #     y = int(pose[i][0] * height)
                
            #     msg[i*2] = pose[i][1]    # x
            #     msg[i*2 +1] = pose[i][0] # y
                
                # cv2.circle(frame, (x, y), 5, (0, 255, 0), 3)

            terminate_t = timeit.default_timer()
            time_diff = str(int(1/(terminate_t - start_t )))
            
            # cv2.putText(frame, "FPS : " + time_diff, (80, 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            
            ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY),30])
            message = pickle.dumps([buffer, time_diff])
            self.client_socket.sendto(message, self.host)
            #print(f"run_1 : {time_diff}")

    def run_0_init(self, cap):
        print("run_0_init >> START")
        while self.flag:
            img, frame = cap.read()

            if not img:
                print("run_0_init >> no frame")
                return
            # start_t = timeit.default_timer()

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resized_img = cv2.resize(frame_rgb, common.input_size(self.interpreter))
            common.set_input(self.interpreter, resized_img)
            self.interpreter.invoke()
            pose = common.output_tensor(self.interpreter, 0).copy().reshape(17, 3)

            height, width, ch = frame.shape

            for i in range(0, 17):
                self.msg[i*2] = 0.0
                self.msg[i*2 +1] = 0.0

                if(pose[i][2] < 0.5):
                    continue
                
                self.msg[i*2] = pose[i][1]
                self.msg[i*2 +1] = pose[i][0]  
    
            # terminate_t = timeit.default_timer()
            # time_diff = str(int(1/(terminate_t - start_t )))

            #print(f"run_0_init : {time_diff}")

    def run_1_init(self, cap):
        print("run_1_init >> START")
        while self.flag:
            img, frame = cap.read()
                
            if not img:
                print("run_1_init >> no frame")
                return

            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            # start_t = timeit.default_timer()

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resized_img = cv2.resize(frame_rgb, common.input_size(self.interpreter))
            common.set_input(self.interpreter, resized_img)
            self.interpreter.invoke()
            pose = common.output_tensor(self.interpreter, 0).copy().reshape(17, 3)

            height, width, ch = frame.shape

            for i in range(0, 17):
                self.msg[i*2] = 0.0
                self.msg[i*2 +1] = 0.0

                if(pose[i][2] < 0.5):
                    continue
                
                self.msg[i*2] = pose[i][1]
                self.msg[i*2 +1] = pose[i][0]
            # terminate_t = timeit.default_timer()
            # time_diff = str(int(1/(terminate_t - start_t )))

            #print(f"run_1_init : {time_diff}")

    
    def run(self):
        cap = cv2.VideoCapture("/dev/video1")
        while 1:
            # INIT 모드, 위치 조정
            self.event.wait()
            self.event.clear()
            self.flag = True
            sleep(1)
            print(f"Video Start >> INIT {self.modes}")

            if self.modes[0] == 0:
                self.run_0_init(cap)
            elif self.modes[0] == 1:
                self.run_1_init(cap)
            
            # RUN 모드, 운동 시작
            self.event.wait()
            self.event.clear()
            self.flag = True
            sleep(1)
            print(f"Video Start >> RUN {self.modes}")

            if self.modes[0] == 0:
                self.run_0(cap)
            elif self.modes[0] == 1:
                self.run_1(cap)

            print("Video Done >> WAIT")
            
        print("Video Exit")
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    pass
