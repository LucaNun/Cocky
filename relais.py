import RPi.GPIO as GPIO
import time


class Relais():
    #Initalisiert das Relais, Pin sowie der Modus wird gesetzt
    def __init__(self, pin):
        self.pin = pin
        #Vergibt die Pinnummern nach der GPIO-Pin Bezeichnung
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        #Setzt den GPIO-Pin auf Output
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

    #Schaltet das Relais an
    def an(self):
        GPIO.output(self.pin, GPIO.LOW)

    #Schaltet das Relais aus
    def aus(self):
        GPIO.output(self.pin, GPIO.HIGH)
