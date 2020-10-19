import RPi.GPIO as GPIO
import time

class Flowmeter():
    def __init__():
        self.pin = pin
        self.ml = ml
        self.imp = 0

    def addsome(self, pinnumber):
        self.imp += 1

    def messen(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.addsome)

        self.start = time.time()
        while imp < 1000:
            time.sleep(0.1)
        self.end = time.time()

        '''
        HIER MUSS DER CODE ZUR BESTIMMUNG DER MENGE REIN
        VLLT AUCH HÖHER
        IMP / 73
        ERGEBNIS * DAUER
        = MENGE
        '''
