import flask, asyncio, time, getraenk
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
    g = getraenk.Misschung()
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
        getreankMixen_P = Process(
            target=getreankMixen,
            args=[g.data["Moscow Mule"],],
            daemon=True
        )
        getreankMixen_P.start()
        return "gestartet"


def getreankMixen(args):
    '''
    Über die *args* werden die benötigeten Pumpen und die benötigten Flowmeter,
    sowie die benötigte Menge an Geträng übermittelt
    Es wird eine For Schleife erstellt welche dann
    die benötigten Getränke abarbeitet
    '''
    for line in args[0]["auto"]:
        print("%sml %s wird eingefüllt!" %(args[0]["auto"][line], line))
        '''
        Hier muss die Pumpe angesteuert werden!s
        '''

        # An das Flowmeter muss die Getränkemenge übergeben werden!
        a = asyncio.run(flowmeter(2))

        '''
        Hier muss die Pumpe wieder gestoppt werde!
        '''
        print("%s ist fertig eingefüllt!" %line)
    print("%s ist fertig!" %args[0]["name"])


async def flowmeter(value):
    await asyncio.sleep(value)
    print("Flowmeter raise")


if __name__ == "__main__":
    app.run('localhost', '3333', debug=True)
