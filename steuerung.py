import asyncio
import waegezelle

def pumpen(db, id, bottlesize):
    sql = "SELECT * FROM `mischungen&inhalte` WHERE `Mischungs.ID` = %s" %id
    db.mycursor.execute(sql)
    inhalte = db.mycursor.fetchall()

    for inhalt in inhalte:
        sql = "SELECT `Pumpen.ID`, `Manuell`, `Bezeichnung` FROM `inhalte` WHERE `Inhalts.ID` = %s"%inhalt[1]
        db.mycursor.execute(sql)
        result = db.mycursor.fetchall()

        # Wenn eine Pumpen.ID gesetzt ist
        if not result[0][0] == None:
            #Holt sich den Pin für das Getränk aus der Datenbank
            sql = "SELECT `Pin` FROM `pumpen` WHERE `Pumpen.ID` = %s" %result[0][0]
            db.mycursor.execute(sql)
            pin = db.mycursor.fetchall()

            #Die ml Menge wird aus dem Prozentwert berechnet
            menge = (bottlesize/100) * int(inhalt[2])
            waegezelle.waegezelle(pin[0][0], menge, result[0][2])
