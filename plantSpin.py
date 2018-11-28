# Turn when hand in front

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set variables for the GPIO motor pins

pinMotorAForwards = 10
pinTrigger = 17
pinEcho = 18

# How many time to turn to pin on and off each second
Frequency = 20
# How long the pn stays on each cycle as a percent
DutyCycleA = 90
# Setting the duty cycle to 0 means the motors will not turn
Stop = 0

# Set the GPIO Pin mode
GPIO.setup(pinMotorAForwards, GPIO.OUT)
GPIO.setup(pinTrigger, GPIO.OUT)  # Trigger
GPIO.setup(pinEcho, GPIO.IN)  # Echo

# Distance Variables
HowNear = 15.0
ForwardTime = 2.5

# Set the GPIO to software PWM at 'Frequency' Hertz
pwmMotorAForwards = GPIO.PWM(pinMotorAForwards, Frequency)

# Start the SW PWM with a duty clycle of 0
pwmMotorAForwards.start(Stop)

# Turn all motors off
def StopMotors():
    pwmMotorAForwards.ChangeDutyCycle(Stop)

# Turn both motors forwards
def Forwards():
    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)

# Take a distance measurement
def Measure():
    GPIO.output(pinTrigger, True)
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)
    StartTime = time.time()
    StopTime = StartTime

    while GPIO.input(pinEcho)==0:
        StartTime = time.time()
        StopTime = StartTime

    while GPIO.input(pinEcho)==1:
        StopTime = time.time()
        if StopTime-StartTime >= 0.04:
            print("Too Close!")
            StopTime = StartTime
            break

    ElapsedTime = StopTime - StartTime
    Distance = (ElapsedTime * 34326)/2

    return Distance
    time.sleep(2)

# Return True if the sensor sees an obstacle
def IsNearObstacle(localHowNear):
    Distance = Measure()

    print("IsNearObstacle: "+str(Distance))
    if Distance < localHowNear:
        return True
    else:
        return False

# If true, move
def AvoidObstacle():
    print("Spin the plant!")
    Forwards()
    time.sleep(ForwardTime)
    StopMotors()

try:
    GPIO.output(pinTrigger, False)
    time.sleep(0.1)
    while True:
        StopMotors()
        time.sleep(2)
        if IsNearObstacle(HowNear):
            AvoidObstacle()

except KeyboardInterupt:
    GPIO.cleanup()
