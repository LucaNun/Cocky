from app.main import bp

from flask import render_template, request, redirect, url_for
from app.extensions import mysql

@bp.route('/')
def index():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM mixtures")
    cocktails = con.fetchall()
    print(cocktails)
    return render_template('allCocktails.html', cocktails=cocktails)

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
    
    print(drinks)
    print(pumps)
    return render_template("pumpchange.html", pumps = pumps, drinks = drinks)

