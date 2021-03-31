import flask, database, steuerung
from flask import Flask, request, redirect, url_for, render_template



db = database.Datenbank(host="localhost", user="root", pw="", database_name="cocktail")

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run('192.168.178.65', '3334', debug=True)
