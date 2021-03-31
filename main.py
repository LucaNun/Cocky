#import flask, asyncio, time, getraenk, threading, random, database, steuerung
#from multiprocessing import Process
import flask, database, steuerung
import RPi.GPIO as GPIO
from relais import Relais
from flask import Flask, request, redirect, url_for, render_template



#-Display
#--Aktueller Zustand


#!!!!!!!!!!!!
#?! Die wagge muss auf die prozentzahlen eingestellt werden
# Etwas auslagern in die Classe Datenbank?
# Pumpe neu zuweisen
# -Wenn Pumpe neu zugewiesen würd davor bei allen Inhalten die gleiche Pumpen ID entfernen
# 3D Druck Wagge
#
#!!!!!!!!!!!!

db = database.Datenbank(host="localhost", user="root", pw="root", database_name="cocktail")
#db = database.Datenbank(host="localhost", user="root", pw="", database_name="cocktail")

app = Flask(__name__)

inited_pumps = False
bottlesize = 250

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
def get_drinks():
    #Wenn die Pumpen noch nicht Initalisiert sind führe init_pumps() aus
    if not inited_pumps:
        init_pumps()

    result = db._get_mixdrinks()

    return render_template("getdrinks.html", result=result, len=len(result))

@app.route("/getdrink/<id>", methods=['GET', 'POST'])
def get_drink(id):
    if not inited_pumps:
        init_pumps()

    if request.method == 'GET':
        answer = []
        achtung = False

        sql = "SELECT * FROM `mischungen` WHERE `Mischungs.ID` = '%s'"%id
        db.mycursor.execute(sql)
        mische = db.mycursor.fetchall()
        answer.append("Name: " + str(mische[0][1]) + "<br>Beschreibung:" + str(mische[0][2]) +"<br>")

        sql = "SELECT * FROM `mischungen&inhalte` WHERE `mischungs.id` = '%s'"%mische[0][0]
        db.mycursor.execute(sql)
        belegung = db.mycursor.fetchall()
        #0 = Misch.ID, 1 = Inhalts.ID, 2 = Menge
        #Checke hier ob alle inhalte verfügbar sind
        #wenn nein dann machte es kenntlich auf der seite
        inhalte = []
        for i in range(0,len(belegung)):
            sql = "SELECT `pumpen.id`, `manuell`, `Bezeichnung`, `Beschreibung` FROM `inhalte` WHERE `inhalts.id` = '%s'"%belegung[i][1]
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
def make_drink(id):
    if not inited_pumps:
        init_pumps()

    if request.method == 'GET':
        global bottlesize
        steuerung.pumpen(db, id, bottlesize)
        #-Asyncron Starten

        return redirect("/ready/%s" %id)

@app.route("/ready/<id>", methods=['GET', 'POST'])
def ready(id):
    if not inited_pumps:
        init_pumps()

    sql = "SELECT * FROM `mischungen&inhalte` WHERE `mischungs.id` = '%s'" %id
    db.mycursor.execute(sql)
    inhalte = db.mycursor.fetchall()
    #0 = Misch.ID, 1 = Inhalts.ID, 2 = Menge

    answer = []
    answer.append("<h1>Es fehlen noch folgene Inhalte:</h1>")
    for inhalt in inhalte:
        sql = "SELECT `pumpen.id`, `manuell`, `Bezeichnung` FROM `inhalte` WHERE `inhalts.id` = '%s'" %inhalt[1]
        db.mycursor.execute(sql)
        result = db.mycursor.fetchall()
        if result[0][0] == None or result[0][1] == 1:
            if inhalt[2] == 0:
                answer.append("<h2>%s: Rest auffüllen</h2>" %result[0][2])
            else:
                answer.append("<h2>%s: %s</h2>" %(result[0][2], inhalt[2]))
    answer.append('<a href="/" class="btn btn-primary mt-4">Zurück..</a>')
    return "".join(answer)

@app.route("/newdrink", methods=['GET', 'POST'])
def new_drink():
    if request.method == 'GET':
        return render_template("newdrink.html")
    if request.method == 'POST':
        data = [request.form["Name"], request.form["Beschreibung"], request.form["Alkoholcheck"], request.form["Einfüllung"]]

        if data[2] == "Alkoholfrei":
            data[2] = 0
        else:
            data[2] = 1

        if data[3] == "Automatisch":
            data[3] = 1
        else:
            data[3] = 0
        #!!!!!!!! Bei Bezeichnung fehlt das n Bezeichnung
        sql = "INSERT INTO inhalte (`Inhalts.ID`, `Pumpen.ID`, `Bezeichnung`, `Beschreibung`, `Alkohol`, `Manuell`) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (None, None, data[0], data[1], data[2], data[3])
        db.mycursor.execute(sql, val)
        db.mydb.commit()
        return redirect("/")

@app.route('/newmixdrink', methods=['GET', 'POST'])
def new_mixdrink():
    if request.method == 'GET':
        sql = "SELECT `Inhalts.ID`, `Bezeichnung` FROM `inhalte`"
        db.mycursor.execute(sql)
        result = db.mycursor.fetchall()

        return render_template("newmixdrink.html", liste=result)

    if request.method == 'POST':
        data = request.form
        name = ""
        beschreibung = ""

        for i in data.items():
            if i[0] == 'Mixdrink':
                name = i[1]
            if i[0] == 'Beschreibung':
                beschreibung = i[1]

        sql = "INSERT INTO mischungen (`Mischungs.ID`, `Bezeichnung`, `Beschreibung`) VALUES (%s, %s, %s)"
        val = (None, name, beschreibung)
        db.mycursor.execute(sql, val)
        db.mydb.commit()

        sql = "SELECT `Mischungs.ID` from `mischungen` where `Bezeichnung` = '%s'" %name
        db.mycursor.execute(sql)
        result = db.mycursor.fetchall()

        for i in data.items():
            if i[0] == 'Mixdrink' or i[0] == 'Beschreibung':
                continue

            sql = "INSERT INTO `mischungen&inhalte` (`Mischungs.ID`, `Inhalts.ID`, `Menge`) VALUES (%s, %s, %s)"
            val = (result[0][0], int(i[0]), int(i[1]))
            db.mycursor.execute(sql, val)
            db.mydb.commit()

        return redirect("/")

@app.route("/cleaning", methods=['GET'])
def cleaning():
    if not inited_pumps:
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
        GPIO.output(pin, GPIO.LOW)
    else:
        GPIO.output(pin, GPIO.HIGH)
    return ""

@app.route("/setbottlesize", methods=['GET', 'POST'])
def set_bottlesize():
    if request.method == 'GET':
        return render_template('setbottlesize.html')
    if request.method == 'POST':
        value = request.form['value']
        global bottlesize
        bottlesize = int(value)

        return redirect("/")

@app.route("/changepump", methods=['GET'])
def change_pump():
    sql = "SELECT * FROM `pumpen`"
    db.mycursor.execute(sql)
    pumps = db.mycursor.fetchall()

    sql = "SELECT `Inhalts.ID`, `Pumpen.ID`, `Bezeichnung` FROM `inhalte` WHERE `Manuell` = 0 ORDER BY `Pumpen.ID`"
    db.mycursor.execute(sql)
    drinks = db.mycursor.fetchall()

    return render_template("pumpchange.html", pumps = pumps, drinks = drinks)

@app.route("/changepump/<int:pump>/<int:drink>", methods=['GET'])
def change_pump_id(pump, drink):
    # Um doppelte Belegung eines Getränkes zu verhindert
    sql = "UPDATE `inhalte` SET `Pumpen.ID` = NULL WHERE `Pumpen.ID` = %s"%pump
    db.mycursor.execute(sql)
    db.mydb.commit()

    sql = "UPDATE `inhalte` SET `Pumpen.ID` = %s WHERE `Inhalts.ID` = %s"%(pump, drink)
    db.mycursor.execute(sql)
    db.mydb.commit()

    return ""

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
