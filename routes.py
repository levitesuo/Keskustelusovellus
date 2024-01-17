from app import app
from flask import redirect, render_template, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from users import login_handler, newuser_handler



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/error")
def testerror():
    return render_template("error.html", message = "Testivirhe")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if login_handler(username, password):
            session["username"] = username
        return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
    

@app.route("/newuser", methods=["GET", "POST"])
def createAccaunt():
    if request.method == "GET":
        return render_template("newuser.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat", returnUrl="/newuser")
        if newuser_handler(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Käyttäjänimi varattu.", returnUrl="/newuser")
    

@app.route("/users")
def users():
    result = db.session.execute(text("SELECT * FROM users"))
    users = result.fetchall()
    t = ""
    for u in users:
        t += f"<p>{u.username}"
    return t