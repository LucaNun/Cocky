from app.main import bp

from flask import render_template, request, redirect, url_for, current_app, Response
from app.extensions import mysql
from threading import Thread
import json, time

currentDrink = ""
currentProgress = 0
allCurrentProgress = 0
allProgress = 0
status = 0

@bp.route('/')
def index():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM mixtures")
    cocktails = con.fetchall()
    print(cocktails)
    con.close()
    return render_template('allCocktails.html', cocktails=cocktails)

@bp.route('/make/<id>')
def make(id):
    con = mysql.connection.cursor()
    con.execute(f"SELECT * FROM ingredients INNER JOIN mixtureContents ON mixtureContents.ingredientsID = ingredients.ingredientsID where mixtureContents.mixturesID = {id}")
    ingredients = con.fetchall()
    con.execute(f"SELECT * FROM mixtures WHERE mixturesID = {id}")
    mixture = con.fetchone()
    con.execute(f"SELECT * FROM pumps")
    pumps = con.fetchall()
    con.close()
    bottlesize = current_app.config['BOTTLE_SIZE']
    thread = Thread(target=makeCocktail, args=(ingredients, bottlesize, pumps))
    thread.daemon = True
    thread.start()
    return f"Cocktail wird zubereitet..."

def makeCocktail(ingredients, bottlesize, pumps):
    from hx711 import HX711
    from ..relais import Relais
    import time
    hx = HX711(5,6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(384.76331)
    hx.reset()
    hx.tare()

    global currentDrink, currentProgress, allCurrentProgress, allProgress, status
    currentDrink, currentProgress, allCurrentProgress, allProgress, status = 0,0,0,0,0

    ingredientWithPumpCount = sum(1 for ingredient in ingredients if ingredient['pumpID'] is not None)

    for ingredient in ingredients:
        if ingredient['manual'] == 1 or ingredient['pumpID'] == None:
            continue
        hx.tare()
        
        currentDrink = ingredient['name']
        pumpID = ingredient['pumpID']
        pin = next((pump['pin'] for pump in pumps if pump['pumpID'] == pumpID), None)
        pumpe = Relais(pin)
        
        neededWeight = int(bottlesize/100*ingredient['amount'])

        while True:
            pumpe.on()
            weight = hx.get_weight()
            try:
                procent = int((weight/neededWeight)*100)
            except ZeroDivisionError:
                procent = 0
            if procent >= 0:
                currentProgress = procent
                allCurrentProgress = int(allProgress + ((100/ingredientWithPumpCount)/100*currentProgress))
            
            if weight >= neededWeight:
                allProgress += int(100/ingredientWithPumpCount)
                allCurrentProgress = allProgress
                currentProgress = 0
                pumpe.off()
                break
            time.sleep(0.5)
    status = 1
    hx.cleanup()
    time.sleep(0.6)
    currentDrink, currentProgress, allCurrentProgress, allProgress, status = 0,0,0,0,0

@bp.route('/cocktail/<id>')
def getCocktail(id):
    con = mysql.connection.cursor()
    con.execute(f"SELECT * FROM ingredients INNER JOIN mixtureContents ON mixtureContents.ingredientsID = ingredients.ingredientsID where mixtureContents.mixturesID = {id}")
    ingredients = con.fetchall()
    con.execute(f"SELECT * FROM mixtures WHERE mixturesID = {id}")
    mixture = con.fetchone()
    con.close()
    bottlesize = current_app.config['BOTTLE_SIZE']
    return render_template('cocktail.html', ingredients=ingredients, bottlesize=bottlesize, mixture=mixture)

@bp.route("/changepump", methods=['GET', 'POST'])
def change_pump():
    con = mysql.connection.cursor()

    if request.method == 'POST':
        pumpID = request.form.get('pumpID')
        ingredientsID = request.form.get('ingredientsID')
        con.execute(f"UPDATE ingredients SET pumpID=NULL where pumpID = {pumpID}")
        con.execute(f"UPDATE ingredients SET pumpID={pumpID} where ingredientsID = {ingredientsID}")
        mysql.connection.commit()
        return ""
    
    con.execute("SELECT * FROM ingredients where manual = 0")
    drinks = con.fetchall()
    con.execute("SELECT * FROM pumps")
    pumps = con.fetchall()
    con.close()
    return render_template("pumpchange.html", pumps = pumps, drinks = drinks)

@bp.route('/progress')
def get_progress():
    def generate():
        global currentDrink, currentProgress, allCurrentProgress, allProgress, status
        while allProgress <= 100:
            yield f"data:{json.dumps({'allCurrentProgress': allCurrentProgress, 'currentProgress': currentProgress, 'currentDrink': currentDrink, 'status': status})}\n\n"
            time.sleep(0.5)
    return Response(generate(), mimetype='text/event-stream')
