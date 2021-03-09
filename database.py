import mysql.connector

#! Hier muss nochmal durch geguckt werden und KOMMENTIERT werden!!

class Datenbank():

    def __init__(self, host, user, pw, database_name):
        self.host = host
        self.user = user
        self.pw = pw
        self.database_name = database_name

        try:
            self._Create_database("cocktail")
        except:
            self.mydb = self._Connect()
            self.mycursor = self.mydb.cursor()

    def _Connect(self):
        return mysql.connector.connect(
          host=self.host,
          user=self.user,
          passwd=self.pw,
          database=self.database_name)


    def _Create_database(self, database_name):
        self.mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.pw)

        self.mycursor = self.mydb.cursor()
        sql = "Create DATABASE `%s`" %database_name
        self.mycursor.execute(sql)
        print("Database %s created!" %database_name)

    def _Create_tabel(self, name, sql):
        self.mycursor.execute(sql)
        print("Tabel %s created!" %name)


    def _Regestration_user(self, data):
        sql = "INSERT INTO user (ID, Secondname, Firstname, EMail, Password, Username, Nummber) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = ("NULL", data[0], data[1], data[2], data[3], data[4], data[5])
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def _get_Mischung(self, name):
        pass

    def _get_MischungsInhalte(self, mischungsID):
        sql = "SELECT `Inhalts.ID`, `Menge` FROM `mischungen&inhalte` WHERE `Mischungs.ID` LIKE %s" %mischungsID
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def get_Test(self,name):
        sql = "SELECT `Inhalts.ID`, `Menge` FROM `mischungen&inhalte` WHERE `Mischungs.ID` LIKE (SELECT `Mischungs.ID` FROM `mischungen` WHERE `Bezeichung` LIKE '%s')"%name
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def _get_Inhalt_Pumpe(self, id):
        sql = 'SELECT `Pumpen.ID` FROM `inhalte` WHERE `Inhalts.ID` LIKE %s' %id
        self.mycursor.execute(sql)
        pumpe = self.mycursor.fetchall()[0][0]
        return pumpe

    def _get_Pumpen_Pin(self, id):
        print("ID: " + str(id))
        sql = 'SELECT `PIN` FROM `pumpen` WHERE `Pumpen.ID` LIKE %s' %id
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()[0][0]
