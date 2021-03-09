#import flask, asyncio, time, getraenk, threading, random, database, steuerung
#from multiprocessing import Process
import flask, database, steuerung
import RPi.GPIO as GPIO
from relais import Relais
from flask import Flask, request, redirect, url_for, render_template


#-Webseite
#--Getränk hinzufügen
#--Getränk auswählen
#-Display
#--Aktueller Zustand
#-Flowmeter
#-Pumpensteuerung
#-Reinigungsprogramm

db = database.Datenbank(host="localhost", user="root", pw="root", database_name="cocktail")
#db = database.Datenbank(host="localhost", user="root", pw="", database_name="cocktail")

app = Flask(__name__)
inited_pumps = False

'''
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
        M = getraenk.Mischungen()
        global mischung
        mischung = getraenk.Mischung("Moscow Mule", M)
        # Startet Asyncrone Funktion
        mischung.check()
        getreankMixen_P = Process(
            target=mischung.getreankMixen,
            args=(),
            daemon=True
        )
        getreankMixen_P.start()
        return "gestartet"

'''
@app.route("/", methods=['GET'])
def main():
    #Wenn die Pumpen noch nicht Initalisiert sind führe init_pumps() aus
    if not inited_pumps:
        init_pumps()

    #Gibt die Startseite aus.
    return render_template("main.html")

@app.route("/getdrinks", methods=['GET', 'POST'])
def getdrinks():
    if not inited_pumps:
        init_pumps()

    if request.method == 'GET':
        sql = "SELECT * FROM `mischungen`"
        db.mycursor.execute(sql)
        result = db.mycursor.fetchall()
        answer = ["<h1>Wählen sie ihre Mischung</h1>"]

        for i in range(0, len(result)):
            a = ("<a href='/getdrink/%s'>%s</a><h4>%s</h4><br><br>"%(result[i][1],result[i][1],result[i][2]))
            answer.append(a)
        return "".join(answer)
    elif request.method == 'POST':
        pass

@app.route("/getdrink/<name>", methods=['GET', 'POST'])
def getdrink(name):
    if not inited_pumps:
        init_pumps()

    if request.method == 'GET':
        answer = []
        achtung = False

        sql = "SELECT * FROM `mischungen` WHERE `Bezeichung` = '%s'"%name
        db.mycursor.execute(sql)
        mische = db.mycursor.fetchall()
        answer.append("Name: " + str(mische[0][1]) + "<br>Beschreibung:" + str(mische[0][2]) +"<br>")

        sql = "SELECT * FROM `mischungen&inhalte` WHERE `mischungs.id` = '%s'"%mische[0][0]
        db.mycursor.execute(sql)
        belegung = db.mycursor.fetchall()
        #0 = Misch.ID, 1 = Inhalts.ID, 2 = Menge
        #Checke hier ob alle inhalte verfügbar sind
        #wenn nein dann mach6e es kenntlich auf der seite
        inhalte = []
        for i in range(0,len(belegung)):
            sql = "SELECT `pumpen.id`, `manuell`, `Bezeichung`, `Beschreibung` FROM `inhalte` WHERE `inhalts.id` = '%s'"%belegung[i][1]
            db.mycursor.execute(sql)
            result = db.mycursor.fetchall()

            if result[0][0] == None and result[0][1] == 0:
                inhalte.append((result[0][2], result[0][3], True))
            else:
                inhalte.append((result[0][2], result[0][3], False))
        achtung = False
        for i in range(0, len(inhalte)):
            #Checkt ob ein Getränk fehlt, falls ja färbt er diesen Rot
            if inhalte[i][2]:
                achtung = True
                answer.append("<br><div style='color:red;'><h1>%s</><h2>%s</h2></div>"%(inhalte[i][0],inhalte[i][1]))
            else:
                answer.append("<br><div style='color:green;'><h1>%s</><h2>%s</h2></div>"%(inhalte[i][0],inhalte[i][1]))

        #Wenn ein Getränk fehlt ändert sich der Bestätigungstext
        if achtung:
            answer.append("<br><a href='/makedrink/%s'>Wollen sie wirklich mischen?</a>"%mische[0][0])
        else:
            answer.append("<br><a href='/makedrink/%s'>Jetzt mischen!</a>"%mische[0][0])
        return "".join(answer)

@app.route("/makedrink/<id>", methods=['GET', 'POST'])
def makedrink(id):
    if not inited_pumps:
        init_pumps()

    if request.method == 'GET':
        steuerung.pumpen(db, id)
        #-Asyncron Starten
        #-liste von Inhalten
        #-Liste durchgehen
        #--Wägezelle Starten
        #--Pumpe Starten
        #--wenn wägezelle fertig
        #--Pumpe stoppen
        return redirect("/ready/%s" %id)

@app.route("/cleaning", methods=['GET'])
def cleaning():
    if not inited_pumps:
        print("Initalisieren")
        init_pumps()

    #Hollt die Pumpennummer sowie die Pinnummer aus der Datenbank
    sql = "SELECT * FROM `pumpen`"
    db.mycursor.execute(sql)
    result = db.mycursor.fetchall()

    #Checkt ob eine pumpe an ist
    for i in range(0, len(result)):
        if GPIO.input(result[i][1]):
            result[i] = result[i][0], result[i][1], False
        else:
            result[i] = result[i][0], result[i][1], True

    return render_template("cleaning.html", result=result)

@app.route("/cleaning/<int:pin>", methods=['GET'])
def cleaning_pump(pin):
    if GPIO.input(pin):
        print("Anschalten: " + str(pin))
        GPIO.output(pin, GPIO.LOW)
    else:
        print("Ausschalten: " + str(pin))
        GPIO.output(pin, GPIO.HIGH)
    return ""

@app.route("/ready/<id>", methods=['GET', 'POST'])
def ready(id):
    if not inited_pumps:
        init_pumps()

    sql = "SELECT * FROM `mischungen&inhalte` WHERE `mischungs.id` = '%s'"%id
    db.mycursor.execute(sql)
    inhalte = db.mycursor.fetchall()
    #0 = Misch.ID, 1 = Inhalts.ID, 2 = Menge

    answer = []
    answer.append("<h1>Es fehlen noch folgene Inhalte:</h1>")
    for inhalt in inhalte:
        sql = "SELECT `pumpen.id`, `manuell`, `Bezeichung` FROM `inhalte` WHERE `inhalts.id` = '%s'"%inhalt[1]
        db.mycursor.execute(sql)
        result = db.mycursor.fetchall()
        if result[0][0] == None or result[0][1] == 1:
            if inhalt[2] == 0:
                answer.append("<h2>%s: Rest auffüllen</h2>" %result[0][2])
            else:
                answer.append("<h2>%s: %s</h2>" %(result[0][2], inhalt[2]))
    return "".join(answer)

@app.route("/newdrink", methods=['GET', 'POST'])
def newdrink():
    if request.method == 'GET':
        return render_template("newdrink.html")
    if request.method == 'POST':
        data = [request.form["Name"], request.form["Beschreibung"], request.form["Alkoholcheck"], request.form["Einfüllung"]]
        print("data: "+ str(data))

        if data[2] == "Alkoholfrei":
            data[2] = 0
        else:
            data[2] = 1

        if data[3] == "Automatisch":
            data[3] = 1
        else:
            data[3] = 0
        #!!!!!!!! Bei Bezeichnung fehlt das n Bezeichung
        sql = "INSERT INTO inhalte (`Inhalts.ID`, `Pumpen.ID`, `Bezeichung`, `Beschreibung`, `Alkohol`, `Manuell`) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (None, None, data[0], data[1], data[2], data[3])
        db.mycursor.execute(sql, val)
        db.mydb.commit()
        return redirect("/")

@app.route("/test", methods=['GET', 'POST'])
def test():
    cocktail = test()
    mix = Process(
        target=cocktail.getreankMixen,
        args=(),
        daemon=True
    )
    getreankMixen_P.start()

def init_pumps():
    #Hollt die Pumpennummer sowie die Pinnummer aus der Datenbank
    sql = "SELECT * FROM `pumpen`"
    db.mycursor.execute(sql)
    result = db.mycursor.fetchall()
    #Initalisiert alle Pumpen zum ersten mal
    for i in range(0, len(result)):
        Relais(result[i][1])
    #Holt sich die Globale Variable inited_pumps und setzt diese auf True
    global inited_pumps
    inited_pumps = True

if __name__ == "__main__":
    app.run('192.168.178.48', '3334', debug=True)
    #app.run('192.168.178.65', '3334', debug=True)
