import mysql.connector

class Datenbank():

    def __init__(self, host, user, pw, database_name):
        self.host = host
        self.user = user
        self.pw = pw
        self.database_name = database_name

        self.mydb = self._Connect()
        self.mycursor = self.mydb.cursor()

    def _Connect(self):
        return mysql.connector.connect(
          host=self.host,
          user=self.user,
          passwd=self.pw,
          database=self.database_name)


    # Table mischungen
    def _get_mixdrinks(self):
        sql = "SELECT * FROM `mischungen`"
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def _get_mixdrink(self, id):
        sql = "SELECT * FROM `mischungen` WHERE `Mischungs.ID` = '%s'"%id
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def _insert_mixdrink(self,val):
        sql = "INSERT INTO mischungen (`Mischungs.ID`, `Bezeichnung`, `Beschreibung`) VALUES (%s, %s, %s)"
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def _get_mischungsID_by_Name(self, name):
        sql = "SELECT `Mischungs.ID` from `mischungen` where `Bezeichnung` = '%s'" %name
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    # Table mischungen&inhalte
    def _get_MischungsInhalte_all(self, mischungsID):
        self.mycursor.execute(sql)
        sql = "SELECT * FROM `mischungen&inhalte` WHERE `mischungs.id` = '%s'" %id
        return self.mycursor.fetchall()

    def _get_MischungsInhalte(self, mischungsID):
        sql = "SELECT `Inhalts.ID`, `Menge` FROM `mischungen&inhalte` WHERE `Mischungs.ID` LIKE %s"%mischungsID
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def _insert_mischungs_inhalte(self, val):
        sql = "INSERT INTO `mischungen&inhalte` (`Mischungs.ID`, `Inhalts.ID`, `Menge`) VALUES (%s, %s, %s)"
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    # Table inhalte
    def _get_inhalte(self, inhaltsID):
        sql = "SELECT `pumpen.id`, `manuell`, `Bezeichnung`, `Beschreibung` FROM `inhalte` WHERE `inhalts.id` = '%s'"%inhaltsID
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def _get_inhalte_too(self):
        sql = "SELECT `Inhalts.ID`, `Bezeichnung` FROM `inhalte`"
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def _get_inhalte_change(self):
        sql = "SELECT `Inhalts.ID`, `Pumpen.ID`, `Bezeichnung` FROM `inhalte` WHERE `Manuell` = 0 ORDER BY `Pumpen.ID`"
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def _insert_inhalt(self, val):
        sql = "INSERT INTO inhalte (`Inhalts.ID`, `Pumpen.ID`, `Bezeichnung`, `Beschreibung`, `Alkohol`, `Manuell`) VALUES (%s, %s, %s, %s, %s, %s)"
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    # Table pumpe
    def _get_pumpen(self):
        sql = "SELECT * FROM `pumpen`"
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def _update_pumpID_null(self, pump):
        sql = "UPDATE `inhalte` SET `Pumpen.ID` = NULL WHERE `Pumpen.ID` = %s"%pump
        self.mycursor.execute(sql)
        self.mydb.commit()

    def _update_pumpID(self, pump, drink):
        sql = "UPDATE `inhalte` SET `Pumpen.ID` = %s WHERE `Inhalts.ID` = %s"%(pump, drink)
        self.mycursor.execute(sql)
        self.mydb.commit()
