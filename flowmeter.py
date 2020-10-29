import RPi.GPIO as GPIO
import time

class Flowmeter():
    def __init__(pin, ml):
        self.pin = pin
        self.ml = ml
        self.imp = 0
        self.menge = 0

    def addsome(self, pinnumber):
        self.imp += 1

    def messen(self, menge_needed):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.addsome)

        self.start = time.time()
        while True:
            self.end = time.time()
            self.dauer = self.end - self.start
            self.menge = (self.imp / 73) * self.dauer
            time.sleep(0.01)
            self.imp += 1
            if self.menge >= menge_needed:
                break


        '''
        HIER MUSS DER CODE ZUR BESTIMMUNG DER MENGE REIN
        VLLT AUCH HÖHER
        IMP / 73
        ERGEBNIS * DAUER
        = MENGE
        '''
