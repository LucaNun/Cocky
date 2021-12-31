import flask, database, steuerung
#import RPi.GPIO as GPIO
from relais import Relais
from flask import Flask, request, redirect, url_for, render_template
from threading import Thread


#db = database.Datenbank(host="localhost", user="root", pw="root", database_name="cocktail")
db = database.Datenbank(host="localhost", user="root", pw="", database_name="cocktail")

app = Flask(__name__)

inited_pumps = True#!False
bottlesize = 250
current_drink = []

@app.route("/current", methods=['GET'])
def current():
    return str(values.current_drink)

@app.route("/", methods=['GET'])
def main():
    #Wenn die Pumpen noch nicht Initalisiert sind führe init_pumps() aus
    if not inited_pumps:
        init_pumps()

    #Rendert ein HTML Template
    return render_template("main.html")

@app.route("/getdrinks", methods=['GET', 'POST'])
def get_drinks():
    if not inited_pumps:
        init_pumps()

    result = db._get_mixdrinks()
    r = []
    for drink in result:
        drink = list(drink)
        inhalte = []
        zutaten = db._get_drink(drink[0])
        for zutat in zutaten:
            inhalte.append(list(zutat))
        r.append(drink + [inhalte])
    print(r)
    return render_template("getdrinks.html", result=r, len=len(r))

@app.route("/makedrink/<id>", methods=['GET', 'POST'])
def make_drink(id):
    if not inited_pumps:
        init_pumps()

    if request.method == 'GET':
        global bottlesize
        #Startet es Asyncron als Thread damit nicht mehrmals auf Mischen gedrückt werden kann
        thread = Thread(target=steuerung.pumpen, args=(db, id, bottlesize,))
        thread.daemon = True
        thread.start()

        return redirect("/ready/%s" %id)

@app.route("/ready/<id>", methods=['GET', 'POST'])
def ready(id):
    if not inited_pumps:
        init_pumps()

    inhalte = db._get_MischungsInhalte_all(id)
    #0 = Misch.ID, 1 = Inhalts.ID, 2 = Menge
    print(inhalte)

    rest = []
    manuell = []
    for inhalt in inhalte:
        result = db._get_inhalte(inhalt[1])
        if result[0][0] == None or result[0][1] == 1:
            if inhalt[2] == 0:
                rest.append(result[0][2])
            else:
                manuell.append([result[0][2], inhalt[2]])

    rb = False
    mb = False
    if rest:
        rb = True
    if manuell:
        mb=True
    return render_template("ready.html", r=rest, m=manuell, rb=rb, mb=mb)

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

        val = (None, None, data[0], data[1], data[2], data[3])
        db._insert_inhalt(val)

        return redirect("/")

@app.route('/newmixdrink', methods=['GET', 'POST'])
def new_mixdrink():
    if request.method == 'GET':
        result = db._get_inhalte_too()

        return render_template("newmixdrink.html", liste=result)

    if request.method == 'POST':
        data = request.form
        #name = ""
        #beschreibung = ""

        for i in data.items():
            if i[0] == 'Mixdrink':
                name = i[1]
            if i[0] == 'Beschreibung':
                beschreibung = i[1]

        val = (None, name, beschreibung)
        db._insert_mixdrink(val)

        result = db._get_mischungsID_by_Name(name)

        for i in data.items():
            if i[0] == 'Mixdrink' or i[0] == 'Beschreibung':
                continue

            val = (result[0][0], int(i[0]), int(i[1]))
            db._insert_mischungs_inhalte(val)

        return redirect("/")

@app.route("/cleaning", methods=['GET'])
def cleaning():
    if not inited_pumps:
        init_pumps()

    #Hollt die Pumpennummer sowie die Pinnummer aus der Datenbank
    result = db._get_pumpen()

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
    pumps = db._get_pumpen()
    drinks = db._get_inhalte_change()

    return render_template("pumpchange.html", pumps = pumps, drinks = drinks)

@app.route("/changepump/<int:pump>/<int:drink>", methods=['GET'])
def change_pump_id(pump, drink):
    # Um doppelte Belegung eines Getränkes zu verhindert
    db._update_pumpID_null(pump)

    db._update_pumpID(pump, drink)

    return ""

def init_pumps():
    result = db._get_pumpen()
    #Initalisiert alle Pumpen zum ersten mal
    for i in range(0, len(result)):
        Relais(result[i][1])
    #Holt sich die Globale Variable inited_pumps und setzt diese auf True
    global inited_pumps
    inited_pumps = True

if __name__ == "__main__":
    app.run('localhost', '3334', debug=True)
    #app.run('172.16.1.127', '3334', debug=True)
    #app.run('192.168.178.65', '3334', debug=True)
