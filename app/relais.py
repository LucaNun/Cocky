import RPi.GPIO as GPIO

class Relais():
    def __init__(self, pin):
        self.pin = pin
        #Assigns the pin numbers according to the GPIO pin designation
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        #Set pin to output
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

    def on(self):
        #Set pin to on
        GPIO.output(self.pin, GPIO.LOW)

    def off(self):
        #Set pin to off
        GPIO.output(self.pin, GPIO.HIGH)
