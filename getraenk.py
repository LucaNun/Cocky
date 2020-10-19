import json

class Misschung(object):
    def __init__(self):
        with open("misschungen.json") as f:
            self.liste = json.load(f)

        with open("misschungen.json", "w") as f:
            #s = {"Getreank1":["Hier", "steht", "was"]}
            f.write(json.dumps(self.liste, indent = 2, sort_keys=True))
    def check(self, name, data):
        ## TODO: DATA muss noch übergeben werden
        # Überlegung ob die Classe in der Main.py importiert wird und das von
        # Hier die pumpen angesteuert werden?!

        # Checkt ob alle getraenke vorhanden sind um den drink zu misschen!
        for i in self.liste:
            if i == name:
                for g in self.liste[i][0]["auto"]:
                    if not g in data:
                        return False
                return True
            else:
                return False

class Getraenke():
    def __init__(self):
        with open("getraenke.json") as f:
            self.liste = json.load(f)

        with open("getraenke.json", "w") as f:
            #s = {"Getreank1":["Hier", "steht", "was"]}
            f.write(json.dumps(self.liste, indent = 2, sort_keys=False))

if __name__ == "__main__":
    g = Getraenke()
    e = Misschung()
    # e.check muss auf g.liste angepasst werden
    print(e.check("Gin Tonic", g.liste))
