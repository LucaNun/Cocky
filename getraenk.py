import json

class Misschung(object):
    def __init__(self):
        with open("misschungen.json") as f:
            self.data = json.load(f)

        with open("misschungen.json", "w") as f:
            #s = {"Getreank1":["Hier", "steht", "was"]}
            f.write(json.dumps(self.data, indent = 2, sort_keys=True))

class Getraenke():
    def __init__(self):
        with open("misschungen.json") as f:
            self.data = json.load(f)

        with open("misschungen.json", "w") as f:
            #s = {"Getreank1":["Hier", "steht", "was"]}
            f.write(json.dumps(self.data, indent = 2, sort_keys=True))

if __name__ == "__main__":
    g = Misschung()
