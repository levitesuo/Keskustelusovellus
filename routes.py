from app import app
from flask import redirect, render_template, request, session
from sqlalchemy.sql import text

from flask_sqlalchemy import SQLAlchemy
from os import getenv

from werkzeug.security import check_password_hash, generate_password_hash

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT user_id, password FROM users WHERE username=:username"
        result = db.session.execute(text(sql), {'username':username})
        user = result.fetchone()
        if not user:
            #To do invalid username
            pass
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = username
            else:
                #to do invalid password
                pass
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
        if password1 == password2:
            hash_value = generate_password_hash(password1)
            sql = f"INSERT INTO users (username, password) VALUES (:username, :password);"
            db.session.execute(text(sql), {'username':username, 'password':hash_value})
            db.session.commit()
        return redirect("/")
    

@app.route("/users")
def users():
    result = db.session.execute(text("SELECT * FROM users"))
    users = result.fetchall()
    t = ""
    for u in users:
        t += f"<p>{u.username}"
    return t