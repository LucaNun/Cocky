#import RPi.GPIO as GPIO

class Relais():
    def __init__(self, pin):
        #Initalisiert das Relais, Pin sowie der Modus wird gesetzt
        self.pin = pin
        #Vergibt die Pinnummern nach der GPIO-Pin Bezeichnung
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        #Setzt den GPIO-Pin auf Output
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

    def an(self):
        #Schaltet das Relais an
        GPIO.output(self.pin, GPIO.LOW)

    def aus(self):
        #Schaltet das Relais aus
        GPIO.output(self.pin, GPIO.HIGH)
