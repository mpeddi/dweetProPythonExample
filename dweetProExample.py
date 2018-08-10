
# dweetPro example Plant Spinner

import RPi.GPIO as GPIO
import time
import datetime
import requests
import json

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set variables for the GPIO motor pins
pinMotorAForwards = 10
# How many times to turn to pin on and off each second
Frequency = 20
# How long the pin stays on each cycle as a percent
DutyCycleA = 90
# Setting the duty cycle to 0 means the motors will not turn
Stop = 0
# Set the GPIO Pin mode
GPIO.setup(pinMotorAForwards, GPIO.OUT)
# Set the GPIO to software PWM at 'Frequency' Hertz
pwmMotorAForwards = GPIO.PWM(pinMotorAForwards, Frequency)
# Start the SW PWM with a duty cycle of 0
pwmMotorAForwards.start(Stop)
# Turn the motor off
def StopMotors():
    pwmMotorAForwards.ChangeDutyCycle(Stop)
# Turn the motor forwards
def Forwards():
    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)

while True:
    Forwards()
    time.sleep(3)
    StopMotors()
    print(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
    time.sleep(30)

    timestamp = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    url = 'https://dweetpro.io:443/v2/dweets'

    dweetheader = { 'X-DWEET-AUTH' : 'eyJyXXXXXXXXXXXXXXXXXXX', 'content-type' : 'application/json'}

    payload_data = {
        "thing": "testie",
        "key": "AsiBr-XXXXXX-XXXXX-XXXXX-XXXXX-XXX-XXX-XXXXX",
        "content": {"Timestamp":str(timestamp) }
      }


    try:
      r = requests.post(url,  data=json.dumps(payload_data), headers = dweetheader) #send json to dweetpro

    except:
      pass


GPIO.cleanup()
