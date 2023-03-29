from time import sleep, time
from threading import Thread
from adafruit_motorkit import MotorKit

# kit = MotorKit()
# kit.motor1.throttle = -1.0
# time.sleep(1)
# kit.motor1.throttle = 0

class Motor(MotorKit, Thread):
    def __init__(self):
        MotorKit.__init__(self)
        Thread.__init__(self)

    def Stop(self):
        self.motor1.throttle = 0
        self.motor2.throttle = 0

    def Go(self, power=0.9):
        self.motor1.throttle = power
        self.motor2.throttle = power

    def Back(self, power=0.9):
        self.motor2.throttle = -power
        self.motor1.throttle = -power
        
#motor1 is Right!
    def LeftTurn(self, power=0.7):
        self.motor1.throttle = power
        self.motor2.throttle = -power

#motor1 is 오른쪽
    def RightTurn(self, power=0.7):
        self.motor2.throttle = power
        self.motor1.throttle = -power

    #def rightDegree(self, degree):
    #    self.

    def run(self):
        pass

    #약 20cm 정도 움직인다
    def Go_2(self, power=0.5):
        for i in range(11):
            sleep(0.2)
            self.motor1.throttle = (1 - (0.1*i)) * power
            self.motor2.throttle = ( 1 - (0.1*i)) * power
        sleep(0.2)

    def Back_2(self, power=0.55):
        for i in range(11):
            sleep(0.2)
            self.motor1.throttle = -(1 - (0.1*i)) * power
            self.motor2.throttle = -( 1 - (0.1*i)) * power
        sleep(0.2)
#조금만 움직여라 3시리즈
    def Go_3(self, power=0.5):
        for i in range(11):
            sleep(0.1)
            self.motor1.throttle = (1 - (0.1*i)) * power
            self.motor2.throttle = ( 1 - (0.1*i)) * power
        sleep(0.2)

    def Back_3(self, power=0.55):
        for i in range(11):
            sleep(0.1)
            self.motor1.throttle = -(1 - (0.1*i)) * power
            self.motor2.throttle = -( 1 - (0.1*i)) * power
        sleep(0.2)

#조금만 움직여라 4시리즈
    def Go_4(self, power=0.5):
        for i in range(11):
            sleep(0.05)
            self.motor1.throttle = (1 - (0.1*i)) * power
            self.motor2.throttle = ( 1 - (0.1*i)) * power
        sleep(0.2)

    def Back_4(self, power=0.55):
        for i in range(11):
            sleep(0.05)
            self.motor1.throttle = -(1 - (0.1*i)) * power
            self.motor2.throttle = -( 1 - (0.1*i)) * power
        sleep(0.2)

#motor1 is 오른쪽
#2시리즈 (약 45도 움직여라)
    def RightTurn_2(self, power=0.35):
        peak_speed = 0
        for i in range(11):
            sleep(0.2)
            self.motor2.throttle = (1 - (0.1*i)) * power
            self.motor1.throttle = -( 1 - (0.1*i)) * power
        sleep(0.2)

    def LeftTurn_2(self, power=0.432):
        peak_speed = 0
        for i in range(11):
            sleep(0.2)
            self.motor1.throttle = (1 - (0.1*i)) * power
            self.motor2.throttle = -( 1 - (0.1*i)) * power
        sleep(0.2)

#motor1 is 오른쪽//
#30도 정도만 움직여라 3시리즈
    def RightTurn_3(self, power=0.35):
        peak_speed = 0
        for i in range(11):
            sleep(0.1)
            self.motor2.throttle = (1 - (0.1*i)) * power
            self.motor1.throttle = -( 1 - (0.1*i)) * power
        sleep(0.2)

    def LeftTurn_3(self, power=0.432):
        peak_speed = 0
        for i in range(11):
            sleep(0.1)
            self.motor1.throttle = (1 - (0.1*i)) * power
            self.motor2.throttle = -( 1 - (0.1*i)) * power
        sleep(0.2)



    """
    def RightTurn_3(self, power=0.42):
        peak_speed = 0
        for i in range(11):
            self.motor2.throttle = (1 - (0.1*i)) * power
            self.motor1.throttle = -( 1 - (0.1*i)) * power
            sleep(0.1)
        sleep(0.2)

    def LeftTurn_3(self, power=0.42):
        peak_speed = 0
        for i in range(11):
            self.motor1.throttle = (1 - (0.1*i)) * power
            self.motor2.throttle = -( 1 - (0.1*i)) * power
            sleep(0.1)
        sleep(0.2)
        """


#motor1 is 오른쪽
#90시리즈 (약 90도 움직여라)
    def RightTurn_90(self, power=0.35):
        peak_speed = 0
        for i in range(11):
            
            self.motor2.throttle = (1 - (0.1*i)) * power
            self.motor1.throttle = -( 1 - (0.1*i)) * power
            if (i == 0):
                sleep(0.65)
            else:
                sleep(0.45)
        sleep(0.2)

    def LeftTurn_90(self, power=0.432):
        peak_speed = 0
        for i in range(11):
            self.motor1.throttle = (1 - (0.1*i)) * power
            self.motor2.throttle = -( 1 - (0.1*i)) * power

            if (i == 0):
                sleep(0.65)
            else:
                sleep(0.45)
        sleep(0.2)




    def ClockWise(self, power=1):
        for i in range(11):
            sleep(1)
            self.motor1.throttle = (1 - (0.1*i)) * power *0.5
            self.motor2.throttle = ( 1 - (0.1*i)) * power 
        sleep(0.2)

    def ClockWise_fast(self, power=1):
        for i in range(11):
            #sleep(1)
            self.motor1.throttle = (1 - (0.1*i)) * power *0.5
            self.motor2.throttle = ( 1 - (0.1*i)) * power 
            if (i == 0):
                sleep(10)
            else:
                sleep(0.5)

    def CClockWise(self, power=1):
        for i in range(11):
            sleep(1)
            self.motor2.throttle = (1 - (0.1*i)) * power *0.5
            self.motor1.throttle = ( 1 - (0.1*i)) * power 
        sleep(0.2)

    def C1(self, power=1):
       for i in range(11):
            #sleep(1)
            self.motor1.throttle = (1 - (0.1*i)) * power *0.4
            self.motor2.throttle = ( 1 - (0.1*i)) * power 
            if (i == 0):
                sleep(11)
            else:
                sleep(0.5)

    def CC1(self, power=1):
       for i in range(11):
            #sleep(1)
            self.motor2.throttle = (1 - (0.1*i)) * power *0.4
            self.motor1.throttle = ( 1 - (0.1*i)) * power 
            if (i == 0):
                sleep(11)
            else:
                sleep(0.5)
    def C2(self, power=1):
       for i in range(11):
            #sleep(1)
            self.motor1.throttle = (1 - (0.1*i)) * power *0.4
            self.motor2.throttle = ( 1 - (0.1*i)) * power 
            if (i == 0):
                sleep(1)
            else:
                sleep(0.5)

    def C3(self, power=1):
        for i in range(11):
            #sleep(1)
            self.motor1.throttle = (1 - (0.1*i)) * power *0.35
            self.motor2.throttle = ( 1 - (0.1*i)) * power 
            if (i == 0):
                sleep(10)
            else:
                sleep(0.5)



aico = Motor()

while 1:
    #cmd, power_in  = input("what to do?").split()
    #power_in = float(power_in)
    cmd = input("what to do>>")
    
    aico.Stop()
    sleep(0.5)
    if (cmd == 'w'):
        print("Go!")
        aico.Go_2()
    elif (cmd == 's'):
        print("Back")
        aico.Back_2()

    elif (cmd == 'ww'):
        print("Go!")
        aico.Go_3()
    elif (cmd == 'ss'):
        print("Back")
        aico.Back_3()

    elif (cmd == 'www'):
        print("Go!")
        aico.Go_4()
    elif (cmd == 'sss'):
        print("Back")
        aico.Back_4()
    elif (cmd == 'a'):
        print("Left")
        aico.LeftTurn_2()
    elif (cmd == 'd'):
        print("Right")
        aico.RightTurn_2()

    elif (cmd == 'aa'):
        print("Left")
        aico.LeftTurn_3()
    elif (cmd == 'dd'):
        print("Right")
        aico.RightTurn_3()


    elif (cmd == "a90"):
        aico.LeftTurn_90()

    elif (cmd == "d90"):
        aico.RightTurn_90()

    elif (cmd == 'x'):
        print("Stop!")
        aico.Stop()
    elif (cmd == 'e'):
        print("ClockWise")
        aico.ClockWise_fast()
    elif (cmd == 'q'):
        print("CClockWise")
        aico.CClockWise()
    elif cmd == 't':
        aico.C1()
    elif cmd == 'y':
        aico.CC1()
    elif cmd == 'u':
        aico.C3()
    else:
        print("Wrong input!")