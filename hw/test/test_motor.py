# # import time
# # import board
# # import pwmio
# # from adafruit_motor import servo
# # import periphery

# # print(dir(board))
# # # create a PWMOut object on Pin PWM3.
# # pwm = pwmio.PWMOut(board.PWM2, duty_cycle= 2 ** 15, frequency=50)

# # # Create a servo object, my_servo.
# # my_servo = servo.Servo(pwm)

# # while True:
# #     for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
# #         my_servo.angle = angle
# #         time.sleep(0.05)
# #     for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
# #         my_servo.angle = angle
# #         time.sleep(0.05)

# # import time
# # from adafruit_servokit import ServoKit

# # kit = ServoKit(channels=8)

# # kit.servo[0].angle = 180
# # time.sleep(1)
# # kit.servo[0].angle = 0

# from __future__ import division
# import time

# # PCA9685모듈을 임포트.
# from adafruit_pca9685 import PCA9685
# import board

# print(dir(board.I2C()))
# pwm = PCA9685(board.I2C(), address=0x60, reference_clock_speed=25000000) #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# pwm.motor1.throttle = 0

# #  서보모터의 펄스 길이를 최소, 중간, 최대로 설정
# servo_min = 130  # Min pulse length out of 4096
# servo_mid = 370  # Middle pulse length out of 4096
# servo_max = 630  # Max pulse length out of 4096

# # 서보 펄스폭을 더 간단하게 만들어주는 함수.
# def set_servo_pulse(channel, pulse):
#     pulse_length = 1000000    # 1,000,000 us per second
#     pulse_length //= 50       # 60 Hz
#     print('{0}us per period'.format(pulse_length))
#     pulse_length //= 4096     # 12 bits of resolution
#     print('{0}us per bit'.format(pulse_length))
#     pulse *= 1000
#     pulse //= pulse_length
#     pwm.set_pwm(channel, 0, pulse)

# # import time
# # from adafruit_servokit import ServoKit

# # # Set channels to the number of servo channels on your kit.
# # # 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
# # kit = ServoKit(channels=8)

# # kit.servo[0].angle = 180
# # kit.continuous_servo[1].throttle = 1
# # time.sleep(1)
# # kit.continuous_servo[1].throttle = -1
# # time.sleep(1)
# # kit.servo[0].angle = 0
# # kit.continuous_servo[1].throttle = 0


# # 서보모터(SG90)에 최적화된 69Hz로 펄스주기를 설정.
# print(dir(pwm))
# pwm.frequency = 50

# while True:
#     pwm.set_pwm(0, 0, servo_min) #0번서로를 펄스길이최소(130)으로 설정.
#     time.sleep(1) # 1초정지.
#     pwm.set_pwm(0, 0, servo_mid)
#     time.sleep(1)
#     pwm.set_pwm(0, 0, servo_max)
#     time.sleep(1)
#     pwm.set_pwm(0, 0, servo_mid)
#     time.sleep(1)

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

from board import SCL, SDA
import busio


from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)


pca = PCA9685(i2c)


pca.frequency = 50


servo00 = servo.Servo(pca.channels[0])
servo14 = servo.Servo(pca.channels[14])
# We sleep in the loops to give the servo time to move into position.
#servo7.angle = 88
servo00.angle = 40
servo14.angle = 88

print("")
print(f" 0번이   위 => 40일때 수평, 165일때 수직")
print(f"14번이 아래 => 88일때 중앙")
print("")
while(1):
    # for i in range(0, 180, 5):
    #     servo7.angle = i
    #     time.sleep(0.01)
    #  0번이   위 => 40일때 수평, 165일때 수직
    # 14번이 아래 => 88일때 중앙
    ch = int(input("채널을 입력하세요 : "))
    command = int(input("각도를 입력하세요 : "))
    if ch == 0:
        servo00.angle = command
    elif ch == 14:
        servo14.angle = command
    # for i in range(180):
    #     servo7.angle = 180 - i
    #     time.sleep(0.03)

    # # You can also specify the movement fractionally.
    # print("start") 
    # fraction = 0.0
    # while fraction < 1.0:
    #     servo7.fraction = fraction
    #     fraction += 0.01
    #     time.sleep(0.03)

pca.deinit()