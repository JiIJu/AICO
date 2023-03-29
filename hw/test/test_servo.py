from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

kit = MotorKit()

for i in range(200):
    kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
kit.stepper1.release()