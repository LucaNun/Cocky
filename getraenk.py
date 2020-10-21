import json

class Misschung():
    def __init__(self):
        with open("misschungen.json") as f:
            self.misschungen = json.load(f)
        with open("pumpen.json") as f:
            self.pumpen = json.load(f)

        with open("misschungen.json", "w") as f:
            f.write(json.dumps(self.misschungen, indent = 2, sort_keys=True))
        with open("pumpen.json", "w") as f:
            f.write(json.dumps(self.pumpen, indent = 2, sort_keys=False))

    def check(self, name):
        if name in self.misschungen:
            # TODO: speicher self.misschungen[name] die getränke in x um
            # die daten mit den pumpen.values abzugleichen und es als
            # return mit pin und sorte zu übergeben

            a = list(self.pumpen.values())
            x = []
            for i in range(len(a)):
                x.append(a[i]["Sorte"])
            # Checkt ob alle Getraenke vorhanden sind um den drink zu misschen
            for g in self.misschungen[name][0]["auto"]:
                if not g in x:
                    return False
            return x
        return "Misschung nicht vorhanden"

    def get_pin(self):
        # Pin und Sorte übergeben?!

        pass

    def pumpen(self, pin):
        pass

if __name__ == "__main__":
    e = Misschung()
    # e.check muss auf g.liste angepasst werden
    print(e.check("Gin Tonic"))
