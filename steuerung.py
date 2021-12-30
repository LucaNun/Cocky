import asyncio
from hx711py import waegezelle

def pumpen(db, id, bottlesize):
    sql = "SELECT * FROM `mischungen&inhalte` WHERE `Mischungs.ID` = %s" %id
    db.mycursor.execute(sql)
    inhalte = db.mycursor.fetchall()
    #0 = Misch.ID, 1 = Inhalts.ID, 2 = Menge

    for inhalt in inhalte:
        sql = "SELECT `Pumpen.ID`, `Manuell`, `Bezeichnung` FROM `inhalte` WHERE `Inhalts.ID` = %s"%inhalt[1]
        db.mycursor.execute(sql)
        result = db.mycursor.fetchall()

        # Wenn keine Pumpen.ID gesetzt ist überspringen
        if result[0][0] == None:
            continue

        else:
            #Holt sich den Pin für das Getränk aus der Datenbank
            sql = "SELECT `Pin` FROM `pumpen` WHERE `Pumpen.ID` = %s" %result[0][0]
            db.mycursor.execute(sql)
            pin = db.mycursor.fetchall()

            #Die ml Menge wird aus dem Prozentwert berechnet
            menge = (bottlesize/100) * int(inhalt[2])
            waegezelle.waegezelle(pin[0][0], menge, result[0][2])

            # Nur wenn zu viel nachläuft
            #time.sleep(2)
