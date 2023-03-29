import time
from adafruit_servokit import ServoKit


while(1):
    servo_num = 1
    ch = int(input())
    kit = ServoKit(channels=ch)
    kit.servo[servo_num].angle = 180
    kit.continuous_servo[servo_num].throttle = 1
    time.sleep(1)

    kit.continuous_servo[servo_num].throttle = -1
    time.sleep(1)

    kit.servo[servo_num].angle = 0
    kit.continuous_servo[servo_num].throttle = 0
