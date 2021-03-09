import RPi.GPIO as GPIO
import time
'''
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT)

status = True
while True:
    if status:
        GPIO.output(11, GPIO.LOW)
        status = False
        time.sleep(7)
    else:
        GPIO.output(11, GPIO.HIGH)
        status = True
        time.sleep(2)
'''
class Relais():
    #Initalisiert das Relais, Pin sowie der Modus wird gesetzt
    def __init__(self, pin):
        self.pin = pin
        #Vergibt die Pinnummern nach der GPIO-Pin Bezeichnung
        GPIO.setmode(GPIO.BCM)
        #? GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

    #Schaltet das Relais an
    def an(self):
        GPIO.output(self.pin, GPIO.LOW)

    #Schaltet das Relais aus
    def aus(self):
        GPIO.output(self.pin, GPIO.HIGH)
