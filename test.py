import flask, asyncio, time, getraenk, threading, random
from multiprocessing import Process
from flask import Flask
from flask_cors import CORS

###
### Test für die Loadbar
###
z = 0
app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def testroute():
    global z
    if z >= 100:
        z = 0
    z+= random.randint(1, 10)
    return str(z)

if __name__ == "__main__":
    app.run('localhost', '3334', debug=True)
