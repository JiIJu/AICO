import time
import board
import pwmio
from adafruit_motor import servo
from periphery import GPIO, PWM


## create a PWMOut object on Pin D5.
#pwm = pwmio.PWMOut("/sys/class/pwm/pwmchip0/pwm0", duty_cycle=2 ** 15,  frequency=50)
# create a PWMOut object on Pin D5.
#pwm = pwmio.PWMOut(32, duty_cycle=2 ** 15,  frequency=50)
pwm = PWM(2, 0)
pwm.frequency = 60


for i in range(50):
    pwm.duty_cycle = 0.05
    pwm.enable()
    time.sleep(0.1)
    print("now s1")

for i in range(50):
    pwm.duty_cycle = 0.15
    pwm.enable()
    time.sleep(0.1)
    print("now s2")
pwm.close()
##############################33
