# Plant Spinner DweetPro

import RPi.GPIO as GPIO
import time
import datetime
import requests
import json

start = datetime.datetime.now()
send_url = 'https://dweetpro.io:443/v2/dweets'
get_url = 'https://dweetpro.io:443/v2/dweets/latest'
dweet_header = { 'X-DWEET-AUTH' : 'eyJyb2XXXXXXXXXXXX51351c3b', 'content-type' : 'application/json'}
thing_name = 'testie'
thing_key = 'AsiBr-XXXXX-XXxxX-XXxxx-xXXXX-Xxxxx-XxxxX-XXxXX-xxxxx-X-XX'

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
    current = datetime.datetime.now()
    diff = current - start
    if int(diff.total_seconds()) % 5 == 0:
        print('5 secs')
        time.sleep(1)
        try:
            ret = requests.get(get_url,  params={"thing":thing_name,"key":thing_key}, headers = dweet_header) #get latest dweet to check if spin toggle requested
            r = ret.json()
            latest = r['with'][0]['content']
            print(latest)
            if 'spin_toggle' in latest:
                if latest['spin_toggle'] == 1:
                    print('toggling spin')
                    timestamp = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                    Forwards()
                    time.sleep(3)
                    StopMotors()
                    reset_payload = {
                        "thing": thing_name,
                        "key": thing_key,
                        "content": {"Timestamp":str(timestamp), "spin_toggle":0 }
                    }
                    t = requests.post(send_url,  data=json.dumps(reset_payload), headers = dweet_header) #send toggle reset
                    time.sleep(1)

        except:
            pass

GPIO.cleanup()
