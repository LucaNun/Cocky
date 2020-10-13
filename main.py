import flask, asyncio, time
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
            args=[{"getränke": ["Cola", "Fanta", "Sprite"]}],
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
    for Getränk in args["getränke"]:
        print("%s wird eingefühlt!" %Getränk)
        '''
        Hier muss die Pumpe angesteuert werden!
        '''

        # An das Flowmeter muss die Getränkemenge übergeben werden!
        a = asyncio.run(flowmeter(2))

        '''
        Hier muss die Pumpe wieder gestoppt werde!
        '''
        print("%s ist fertig eingefühlt!" %Getränk)
    print("Der Drink ist fertig!")


async def flowmeter(value):
    await asyncio.sleep(value)
    print(value)


if __name__ == "__main__":
    app.run('172.16.1.162', '3333', debug=True)
