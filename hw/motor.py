from time import sleep
from threading import Thread
from adafruit_motorkit import MotorKit
from board import SCL, SDA
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from copy import copy

import busio

class Servo():
    def __init__(self):
        i2c = busio.I2C(SCL, SDA)
        self.pca = PCA9685(i2c)
        self.pca.frequency = 50

        self.servo00 = servo.Servo(self.pca.channels[0])
        self.servo14 = servo.Servo(self.pca.channels[14])

    def __del__(self):
        self.pca.deinit()

    def set_state(self, state):
        self.servo14.angle = 88
        if state == 0: #가로모드
            self.servo00.angle = 40
        elif state == 1: #세로모드
            self.servo00.angle = 165

    def set_degree(self, ch, degree):##14번_검은색서보_중앙값:88
        if ch == 0:
            self.servo00.angle = degree
        elif ch == 14:
            self.servo14.angle = degree


class Motor(MotorKit, Thread):
    def __init__(self, event):
        MotorKit.__init__(self)
        Thread.__init__(self)

        self.servo = Servo()
        self.event = event
        self.daemon = True
        self.flag = True
        self.pose = []
        self.modes = [1, 0] # modes[0] 카메라 모드, modes[1] 무브 모드

        self.Stop()

    def __del__(self):
        self.Stop()
    
    def run(self):
        while 1:
            self.event.wait() # 0 이면 가로 1 이면 세로
            self.event.clear()
            print(f"Motor Start >> INIT {self.modes}")
            self.flag = True
            self.servo.set_state(self.modes[0])
            self.motor_main()
            self.event.set()
            sleep(3)

    def Stop(self):
        self.motor2.throttle = 0
        self.motor1.throttle = 0
        
    #이제부터 /test/dcmotor_0207.py의 기능을 이식한다
    #####(5cm)더더 조금만 움직여라 4시리즈
    def Go_4(self, power=0.5):
        for i in range(11):
            sleep(0.05)
            if (i%2 == 1):
                self.motor2.throttle = ( 1.0 - (0.1*i)) * power
                self.motor1.throttle = ( 1.0 - (0.1*i)) * power
            else:
                self.motor1.throttle = ( 1.0 - (0.1*i)) * power
                self.motor2.throttle = ( 1.0 - (0.1*i)) * power
        sleep(0.2)

    def Back_4(self, power=0.55):
        for i in range(11):
            sleep(0.05)
            if (i%2 == 0):
                self.motor1.throttle = -( 1.0 - (0.1*i)) * power
                self.motor2.throttle = -( 1.0 - (0.1*i)) * power
            else:
                self.motor2.throttle = -( 1.0 - (0.1*i)) * power
                self.motor1.throttle = -( 1.0 - (0.1*i)) * power
        sleep(0.2)

    def Back_5(self, power=0.55):
        for i in range(11):
            if (i %2 == 0):
                self.motor1.throttle = -( 1.0 - (0.1*i)) * power
                self.motor2.throttle = -( 1.0 - (0.1*i)) *power
                sleep(0.4)
            else:
                self.motor2.throttle = -( 1.0 - (0.1*i)) * power
                self.motor1.throttle = -( 1.0 - (0.1*i)) *power
                sleep(0.4)
        sleep(0.5)

    def Back_5_C(self, power=0.55):
        for i in range(11):
            if (i %2 == 0):
                self.motor2.throttle = -( 1.0 - (0.1*i)) * power
                self.motor1.throttle = -( 1.0 - (0.1*i)) *power
                sleep(0.4)
            else:
                self.motor1.throttle = -( 1.0 - (0.1*i)) * power
                self.motor2.throttle = -( 1.0 - (0.1*i)) *power
                sleep(0.4)
        sleep(0.5)

    ###############좌/우 제자리 회전기능들#############
    # 90도 정도만 움직여라 90시리즈
    def RightTurn_90(self, power=0.50):
        peak_speed = 0
        for i in range(11):
            self.motor2.throttle = (1.0 - (0.1*i)) * power
            self.motor1.throttle = -( 1.0 - (0.1*i)) * power
            if (i == 0):
                sleep(0.50)
            else:
                sleep(0.40)
        sleep(1)
    def LeftTurn_90(self, power=0.432):
        peak_speed = 0
        for i in range(11):
            self.motor1.throttle = (1.0 - (0.1*i)) * power
            self.motor2.throttle = -( 1.0 - (0.1*i)) * power
            if (i == 0):
                sleep(0.45)
            else:
                sleep(0.45)
        sleep(0.2)
    def LeftTurn_91(self, power=0.432):
        peak_speed = 0
        for i in range(10):
            if (i == 0):
                Factor = (0.8 - (0.1*i))
                self.motor1.throttle = Factor * power
                self.motor2.throttle = -Factor * power
                sleep(0.65)
            elif(i > 0 and i <= 6):
                Factor = (0.8 - (0.1*i))
                self.motor1.throttle = Factor * power
                self.motor2.throttle = -Factor * power
                sleep(0.5)
            else:
                self.motor1.throttle = 0
                self.motor2.throttle = 0
                sleep(0.5)
        sleep(1)
    def RightTurn_91(self, power=0.40):
        peak_speed = 0
        for i in range(10):
            if (i == 0):
                Factor = (0.8 - (0.1*i))
                self.motor1.throttle = Factor * power
                self.motor2.throttle = -Factor * power
                sleep(0.7)
            elif(i > 0 and i < 5):
                Factor = (0.7 - (0.1*i))
                self.motor1.throttle = Factor * power
                self.motor2.throttle = -Factor * power
                sleep(0.5)
            else:
                self.motor1.throttle = 0
                self.motor2.throttle = 0
                sleep(0.5)
        sleep(1)

    ###########1/4원을 그리며 회전하라##########
    # 시계방향C2 //반시계방향CC1
    def C2(self, power=1):
       for i in range(11):
            if (i == 0):
                self.motor1.throttle = (1.0 - (0.1*i)) * power *0.4
                self.motor2.throttle = ( 1.0 - (0.1*i)) * power 
                sleep(11)
            
            elif (i > 0 and i < 8):
                self.motor1.throttle = (1.0 - (0.1*i)) * power *0.4
                self.motor2.throttle = ( 1.0 - (0.1*i)) * power 
                sleep(0.5)

            else:
                self.motor1.throttle = 0
                self.motor2.throttle = 0 
                sleep(0.3)
    ###########/test/dcmotor_0207.py기능들은 여기까지
    ###check기능들
    #사람 정면의 눈과 발목사이를 측정한다
    def Check_10(self):
        now_pose = copy(self.pose)
        #값이 인식되지 않을경우
        if (now_pose[3] == False or now_pose[5] == False or \
            now_pose[31] == False or now_pose[33] == False):
            return -1
        #값이 정확히 인식되었을 경우
        eye_mean = (now_pose[3] + now_pose[5]) / 2.0
        ankle_mean = (now_pose[31] + now_pose[33]) / 2.0
        dist = ankle_mean - eye_mean
        #거리가멀다
        if (dist < 0.6):
            return 1
        #거리가 가깝다
        elif (dist > 0.8):
            return 2
        #적당한 거리이다
        else:
            return 0

    #사람 옆면의 어깨와 발목의 차이를 측정한다
    def Check_11_dist(self):
        now_pose = copy(self.pose)
        #값이 인식되지 않을경우
        if (now_pose[11] == False or now_pose[13] == False or \
            now_pose[31] == False or now_pose[33] == False):
            return -1
        #값이 정확히 인식되었을 경우
        shoulder_mean = (now_pose[11] + now_pose[13]) / 2.0
        ankle_mean = (now_pose[31] + now_pose[33]) / 2.0
        dist = ankle_mean - shoulder_mean
        #거리가멀다
        if (dist < 0.4):
            return 1
        #거리가 가깝다
        elif (dist > 0.6):
            return 2
        #적당한 거리이다
        else:
            return 0

    def Check_11_angle(self):
        now_pose = copy(self.pose)
        #값이 인식되지 않을경우
        if (now_pose[11] == False or now_pose[13] == False):
            return -1
        #값이 정확히 인식되었을 경우
        shoulder_posi = (now_pose[11] + now_pose[13]) / 2.0 
        #왼쪽으로 약간 돌아
        if (shoulder_posi < 0.3):
            return 1
        #오른쪽으로 약간 돌아
        elif (shoulder_posi > 0.5):
            return 2
        #적당한 거리이다 (0.3<shoulder_posi<0.5)
        else:
            return 0
#약 15도 정도만 제자리 회전하는 코드
    def RightTurn_15(self, power=0.35):
        peak_speed = 0
        for i in range(11):
            sleep(0.1)
            self.motor2.throttle = (1 - (0.1*i)) * power
            self.motor1.throttle = -( 1 - (0.1*i)) * power
        sleep(0.2)

    def LeftTurn_15(self, power=0.432):
        peak_speed = 0
        for i in range(11):
            sleep(0.1)
            self.motor1.throttle = (1 - (0.1*i)) * power
            self.motor2.throttle = -( 1 - (0.1*i)) * power
        sleep(0.2)

    ####임송빈이 작성할 코드####
    def motor_main(self):
        if self.modes[0] == 0 and self.modes[1] == 0: # 가로 정면
            pass
        elif self.modes[0] == 0 and self.modes[1] == 1: # 가로 측면
            pass
        elif self.modes[0] == 1 and self.modes[1] == 0: # 세로 정면. 이거하자!!
            self.Back_5()
            self.Back_5_C()
            sleep(1)
            correct_count = 0
            move_list=[]
            move_idx = 0
            while self.flag:
                ret = self.Check_10()
                #적당한 거리
                if (ret == 0):
                    correct_count +=1
                    if (correct_count >= 3):
                        #self.LeftTurn_90()시퀀스가 끝났다는 걸 알려주기 위해서 회전
                        break
                #멀다
                elif (ret == 1):
                    self.Go_4()
                    correct_count=0
                    move_list.append(1)
                    move_idx+=1
                #가깝다
                elif (ret == 2):
                    self.Back_4()
                    correct_count=0
                    move_list.append(0)
                    move_idx+=1
                #값이없으면 무시
                elif (ret == -1):
                    #print("사람인식불가")
                    continue
                if (move_idx >= 4):
                    if (move_list[move_idx-2] != move_list[move_idx-1] and\
                        move_list[move_idx-3] != move_list[move_idx-1] and\
                        move_list[move_idx-4] != move_list[move_idx-1]):
                        break
        # 세로 측면
        elif self.modes[0] == 1 and self.modes[1] == 1: 
            self.LeftTurn_91() #몸체회전
            sleep(1)
            self.servo.set_degree(14, 0)#검은서보모터회전. 카메라를 사용자를 향해 회전
            sleep(2)
            #이제 사용자의 측면으로 이동하라
            print("크게 회전한다")
            self.C2()
            sleep(1)

            self.servo.set_degree(14, 88)
            sleep(2)
            self.servo.set_state(0)
            sleep(3)
            self.RightTurn_90()
            sleep(1)
            # "엎드리세요" 오디오 출력
            #@#이벤트.셋 주석처리
            self.event.set()
            #이제 위치를 조정한다
            # self.Back_5()
            # sleep(1)
            # correct_count = 0
            # move_list=[]
            # move_idx = 0
            # while self.flag:
            #     ret = self.Check_11_dist() # 거리
            #     #적당한 거리
            #     if (ret == 0):
            #         correct_count +=1
            #         if (correct_count >= 3):
            #             break
            #     #멀다
            #     elif (ret == 1):
            #         self.Go_4()
            #         correct_count=0
            #         move_list.append(1)
            #         move_idx+=1
            #     #가깝다
            #     elif (ret == 2):
            #         self.Back_4()
            #         correct_count=0
            #         move_list.append(0)
            #         move_idx+=1
            #     #값이없으면 무시
            #     elif (ret == -1):
            #         #print("사람인식불가")
            #         continue
            #     if (move_idx >= 4):
            #         if (move_list[move_idx-2] != move_list[move_idx-1] and\
            #             move_list[move_idx-3] != move_list[move_idx-1] and\
            #             move_list[move_idx-4] != move_list[move_idx-1]):
            #             break

            # #각도 조정
            # sleep(1)
            # correct_count = 0
            # move_list=[]
            # move_idx = 0
            # while self.flag:
            #     ret = self.Check_11_angle()
            #     #적당한 각도
            #     if (ret == 0):
            #         correct_count +=1
            #         if (correct_count >= 3):
            #             break
            #     #왼쪽으로돌아!
            #     elif (ret == 1):
            #         self.LeftTurn_15()
            #         correct_count=0
            #         move_list.append(1)
            #         move_idx+=1
            #     #오른쪽으로 돌아
            #     elif (ret == 2):
            #         self.RightTurn_15()
            #         correct_count=0
            #         move_list.append(0)
            #         move_idx+=1
            #     #값이없으면 무시
            #     elif (ret == -1):
            #         #print("사람인식불가")
            #         continue
            #     if (move_idx >= 4):
            #         if (move_list[move_idx-2] != move_list[move_idx-1] and\
            #             move_list[move_idx-3] != move_list[move_idx-1] and\
            #             move_list[move_idx-4] != move_list[move_idx-1]):
            #             break