import asyncio
from hx711py import wägezelle

def pumpen(db, id):
    sql = "SELECT * FROM `mischungen&inhalte` WHERE `Mischungs.ID` = %s" %id
    db.mycursor.execute(sql)
    inhalte = db.mycursor.fetchall()
    #0 = Misch.ID, 1 = Inhalts.ID, 2 = Menge


    for inhalt in inhalte:

        print("Inhalt: " + str(inhalt))

        sql = "SELECT `Pumpen.ID`, `Manuell` FROM `inhalte` WHERE `Inhalts.ID` = %s"%inhalt[1]
        db.mycursor.execute(sql)
        result = db.mycursor.fetchall()

        print("result: " + str(result[0]))
        if (result[0][0] == None and result[0][1] == 1) or (result[0][0] == None and result[0][1] == 0):
            print("ERROR")
        else:
            sql = "SELECT `Pin` FROM `pumpen` WHERE `Pumpen.ID` = %s" %result[0][0]
            db.mycursor.execute(sql)
            pin = db.mycursor.fetchall()
            print(str(pin[0][0]))
            wägezelle.waegezelle(pin[0][0], inhalt[2])

            # Nur wenn zu viel nachläuft
            #time.sleep(2)

def reinigen(pin):
    #! Schaltet pumpe an diese nicht schon an ist
    #GPIO.input(24)
    pass
