import flask, asyncio, time, getraenk, threading, random
from multiprocessing import Process
from flask import Flask


#-Webseite
#--Getränk hinzufügen
#--Getränk auswählen
#-Display
#--Aktueller Zustand
#-Flowmeter
#-Pumpensteuerung
#-Reinigungsprogramm

app = Flask(__name__)
@app.route("/", methods=['GET'])
def testroute():
    M = getraenk.Mischungen()
    g = getraenk.Mischung("Moscow Mule", M)
    is_process_existing = "getreankMixen_P" in globals()
    if is_process_existing:
        global getreankMixen_P
        is_process_running = getreankMixen_P.is_alive()
        if is_process_running:
            return "run"
        else:
            del getreankMixen_P
            return "gelöscht"
    else:
        # Startet Asyncrone Funktion
        g.check(M)
        getreankMixen_P = Process(
            target=g.getreankMixen,
            args=(),
            daemon=True
        )
        getreankMixen_P.start()
        return "gestartet"


if __name__ == "__main__":
    app.run('localhost', '3333', debug=True)
