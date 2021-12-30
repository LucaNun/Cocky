#! /usr/bin/python2
def waegezelle(pin, menge, bezeichnung):
    import time
    import sys
    import relais
    import RPi.GPIO as GPIO
    from hx711py.hx711 import HX711

    referenceUnit = 384.76331#390.1

    def cleanAndExit():
        print("Cleaning...")

        if not EMULATE_HX711:
            GPIO.cleanup()

        print("Bye!")
        sys.exit()

    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()

    an = False
    while True:
        try:
            val = hx.get_weight(5)
            if not an:
                pumpe = relais.Relais(pin)
                pumpe.an()
                an = True

            values.current_drink = [bezeichnung, menge, val]

            if int(val) >= int(menge):
                pumpe.aus()
                break

            hx.power_down()
            hx.power_up()
            time.sleep(0.1)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
