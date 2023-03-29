from threading import Thread
import socket
import cv2
import pickle
import timeit

#sudo vim /sys/class/thermal/thermal_zone0/trip_point_4_temp
class Connection(Thread):
    def __init__(self, host_ip, port):
        Thread.__init__(self)
        self.host = (host_ip, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
        print("host name => ", self.host[0])
        print("host port => ", self.host[1])

    def __del__(self):
        self.client_socket.close()
        cv2.destroyAllWindows()

    def run(self):
        while 1:
            cap = cv2.VideoCapture(0)
            print("video start!!")
            while cap.isOpened():
                start_t = timeit.default_timer()
                img, frame = cap.read()
                if not img:
                    print("no frame")
                    continue
                ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY),30])  # ret will returns whether connected or not, Encode image from image to Buffer code(like [123,123,432....])
                
                terminate_t = timeit.default_timer()
                time_diff = str(int(1/(terminate_t - start_t )))
                message = pickle.dumps([buffer, time_diff]) 
                self.client_socket.sendto(message, self.host)
                cv2.imshow("Sending", frame)
                print("sending,,,")
                if cv2.waitKey(1) == 13:
                    break
            cap.release()

if __name__ == "__main__":
    #connection = Connection("192.168.100.37", 10050)
    connection = Connection("192.168.100.106", 10050)
    connection.start()
    connection.join()
