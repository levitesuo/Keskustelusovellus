from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import sys
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/newuser", methods=["GET", "POST"])
def createAccaunt():
    return render_template("newuser.html")

@app.route("/newUserHandler", methods=["POST"])
def newUserHandler():
    username = request.form["username"]
    password = request.form["password"]
    sql = f"INSERT INTO users (username, password, privelages) VALUES ('{username}', '{password}', 'user');"
    result = db.session.execute(text(sql))
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