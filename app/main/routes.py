from app.main import bp

from flask import render_template, request, redirect, url_for, current_app
from app.extensions import mysql

@bp.route('/')
def index():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM mixtures")
    cocktails = con.fetchall()
    print(cocktails)
    con.close()
    return render_template('allCocktails.html', cocktails=cocktails)


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

