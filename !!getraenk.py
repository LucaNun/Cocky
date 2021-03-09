import json, threading, time, asyncio, random#, flowmeter

class Mischung():
    def __init__(self, name, M):
        self.name = name
        self.Mischungen = M

    def check(self):
        if self.name in self.Mischungen.liste:
            a = list(self.Mischungen.pumpen.values())
            x = []
            for i in range(len(a)):
                x.append(a[i]["Sorte"])
            # Checkt ob alle Getraenke vorhanden sind um den drink zu misschen
            for g in self.Mischungen.liste[self.name][0]["auto"]:
                if not g in x:
                    return "Nicht alle Zutaten sind vorhanden!"
            return x
        return "Misschung nicht vorhanden!"

    def getreankMixen(self):
        '''
        Über die *args* werden die benötigeten Pumpen und die benötigten Flowmeter,
        sowie die benötigte Menge an Geträng übermittelt
        Es wird eine For Schleife erstellt welche dann
        die benötigten Getränke abarbeitet
        [{'auto': {Getränk: ML}, 'man':{Getränk: ML }}]
        '''
        print("%s wird gestartet!" %self.name)
        l = []
        for i, line in enumerate(self.Mischungen.liste[self.name][0]['auto']):
            print(str(i) + " " + line)
            t = threading.Thread(target=self.pumpe, args=(line,i))
            t.start()
            l.append(t)

        #Wartet bis jeder Thread fertig durch gelaufen ist
        for i in l:
            while i.is_alive():
                i.join()
                time.sleep(0.1)
        print("%s ist fertig!" %self.name)


    def pumpe(self, line, number):
        print("%sml %s wird eingefüllt!" %(self.Mischungen.liste[self.name][0]['auto'][line], line))
        '''
        Hier muss die Pumpe angesteuert werden!
        '''
        # An das Flowmeter muss die Getränkemenge übergeben werden!
        a = asyncio.run(self.flowmeter(random.randrange(1,5)))
        '''
        Hier muss die Pumpe wieder gestoppt werde!
        '''
        print("%s ist fertig eingefüllt!" %line)

    async def flowmeter(self, value):
        await asyncio.sleep(value)
        print("Flowmeter raise")

    def get_pin(self):
        # Pin und Sorte übergeben?!
        pass
