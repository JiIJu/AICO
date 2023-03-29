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

    def Go(self, power=0.5):
        self.motor1.throttle = power
        self.motor2.throttle = power

    def Back(self, power=0.5):
        self.motor1.throttle = -power
        self.motor2.throttle = -power
#motor1 is Right!
    def LeftTurn(self, power=0.7):
        self.motor1.throttle = power
        self.motor2.throttle = -power
#motor1 is 오른쪽
    def RightTurn(self, power=0.7):
        self.motor2.throttle = power
        self.motor1.throttle = -power

    def rightDegree(self, degree):
        self.

    def run(self):
        pass

aico = Motor()

while 1:
    cmd  = input("what to do?")
    aico.Stop()
    sleep(0.5)
    if (cmd == 'w'):
        print("Go!")
        aico.Go()
    elif (cmd == 's'):
        print("Back")
        aico.Back()
    elif (cmd == 'a'):
        print("Left")
        aico.LeftTurn()
    elif (cmd == 'd'):
        print("Right")
        aico.RightTurn()
    elif (cmd == ' '):
        print("Stop!")
        aico.Stop()
    else:
        print("Wrong input!")

                                    