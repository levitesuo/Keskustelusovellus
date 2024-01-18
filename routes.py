from app import app
from flask import redirect, render_template, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import db_modules.users as users
import db_modules.topics as topics
import db_modules.posts as posts


@app.route("/")
def index():
    t = topics.get_topics()
    return render_template("index.html", content = t)

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
        if not users.login(username, password):
            return render_template("error.html", 
                                   message="Väärä salasana tai käyttäjä", 
                                   returnUrl="/login")
        return redirect("/login")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")
    
@app.route("/newuser", methods=["GET", "POST"])
def createAccaunt():
    if request.method == "GET":
        return render_template("newuser.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if request.form["is_admin"]: 
            is_admin = True
        else:
            is_admin = False 
        if password1 != password2:
            return render_template("error.html",    
                                   message="Salasanat eroavat", 
                                   returnUrl="/newuser")
        if users.register(username, password1, is_admin):
            return redirect("/")
        else:
            return render_template("error.html", 
                                   message="Käyttäjänimi varattu.", 
                                   returnUrl="/newuser")
    
@app.route("/createTopic", methods=["POST"])
def createTopic():
    topic = request.form["topic"]
    topics.create(topic)
    return redirect("/")
    
@app.route("/topic/<int:id>", methods=["GET", "POST"])
def topic(id):
    if request.method == "GET":
        t = topics.get_topic_by_id(id)
        p = posts.get_posts_by_topic(id)
        return render_template("topic.html", t = t, p = p)
    if request.method == "POST":
        topic_id = id
        header = request.form["header"]
        content = request.form["content"]
        posts.new_post(topic_id, header, content)
        return redirect(f"/topic/{id}")
    return "KÄÄK"
    
@app.route("/users")
def userlist():
    result = db.session.execute(text("SELECT * FROM users"))
    users = result.fetchall()
    t = ""
    for u in users:
        t += f"<p>{u.username}"
    return t