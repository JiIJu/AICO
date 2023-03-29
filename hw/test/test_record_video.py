from threading import Thread
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter

import cv2
#import struct
#import imutils
import timeit
import numpy as np

#sudo vim /sys/class/thermal/thermal_zone0/trip_point_4_temp
class Connection(Thread):
    def __init__(self):
        Thread.__init__(self)
        #self.interpreter = make_interpreter('../test_data/movenet_single_pose_lightning_ptq_edgetpu.tflite')
        self.interpreter = make_interpreter('../test_data/movenet_single_pose_thunder_ptq_edgetpu.tflite')
        self.interpreter.allocate_tensors()

    def __del__(self):
        cv2.destroyAllWindows()

    def run(self):
        while 1:
            cap = cv2.VideoCapture(1)
            cnt = 1
            # 웹캠에서 fps 값 획득
            fps = cap.get(cv2.CAP_PROP_FPS)
            print('fps', fps)


            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(width, height)

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(f"./output{cnt}.mp4", fourcc, fps, (width, height))
            print("video start!!")
            f = open(f"./pose_list{cnt}_1.txt", "w")
            f2 = open(f"./pose_list{cnt}_2.txt", "w")
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
                pose = common.output_tensor(self.interpreter, 0).copy().reshape(17, 3)

                height, width, ch = frame.shape

                #msg = []
                # Draw the pose onto the image using blue dots
                for i in range(0, 17):
                    #msg.append(0)
                    #msg.append(0)
                    if(pose[i][2]< 0.5):
                        f.write("0 0 ")
                        f2.write("0 0 ")
                        continue
                    x = int(pose[i][1] * width)
                    y = int(pose[i][0] * height)
                    
                    #msg[i*2] = x
                    #msg[i*2 +1] = y
                    f.write(f"{str(x)} {str(y)} ")
                    f2.write(f"{pose[i][1]} {pose[i][0]} ")

                f.write("\n")
                f2.write("\n")

                terminate_t = timeit.default_timer()
                time_diff = str(int(1/(terminate_t - start_t )))

                writer.write(frame)
                cv2.imshow("RECEIVING...", time_diff))
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()
            cnt = cnt + 1
            f.close()
            f2.close()

if __name__ == "__main__":
    #connection = Connection("192.168.100.37", 10050)
    connection = Connection()
    connection.start()
