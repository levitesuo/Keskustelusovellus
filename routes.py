from app import app
from flask import redirect, render_template, request, session
import db_modules.users as users
import db_modules.topics as topics
import db_modules.posts as posts
import db_modules.comments as comments
import db_modules.privrooms as privrooms


@app.route("/")
def index():
    t = topics.get_topics()
    return render_template("index.html", content = t)

@app.route("/private_test")
def privtest():
    t = topics.get_accessable_private_topics()
    o = []
    for tt in t:
        o.append(tt.header)
    return o

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
        if password1 != password2:
            return render_template("error.html",    
                                   message="Salasanat eroavat", 
                                   returnUrl="/newuser")
        if users.register(username, password1):
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
    
@app.route("/topic/delete/<int:id>")
def deleteTopic(id):
    if not session["is_admin"]:
        return render_template("error.html", 
                                message="Ei sallittu.", 
                                returnUrl="/")
    topics.delete_topic_by_id(id)
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

@app.route("/post/delete/<int:id>")
def deletepost(id):
    post = posts.get_post_by_id(id)
    if not session["is_admin"] or post.owner_id != session["user_id"]:
        return render_template("error.html", 
                                message="Ei sallittu.", 
                                returnUrl="/")
    posts.delete_post_by_id(id)
    return redirect(f"/topic/{post.topic_id}")

@app.route("/post/modify/<int:id>", methods=["GET", "POST"])
def modifypost(id):
    post = posts.get_post_by_id(id)
    if (not session["is_admin"]) and post.owner_id != session["user_id"]:
        return render_template("error.html", 
                                message="Ei sallittu.", 
                                returnUrl="/")
    if request.method == "GET":
        return render_template("modifypost.html", post = post)
    if request.method == "POST":
        header = request.form["header"]
        content = request.form["content"]
        posts.modify_post_by_id(id, content, header)
        return redirect(f"/topic/{post.topic_id}")
    

@app.route("/post/<int:id>", methods=["GET", "POST"])
def post(id):
    if request.method == "GET":
        p = posts.get_post_by_id(id)
        c = comments.get_comments_by_post(id)
        return render_template("post.html", p = p, c = c)
    if request.method == "POST":
        post_id = id
        content = request.form["content"]
        comments.new_comment(post_id,  content)
        return redirect(f"/post/{id}")
    
@app.route("/comment/delete/<int:id>")
def deletecomment(id):
    comment = comments.get_comment_by_id(id)
    if (not session["is_admin"]) and comment.owner_id != session["user_id"]:
        return render_template("error.html", 
                                message="Ei sallittu.", 
                                returnUrl="/")
    comments.delete_comment_by_id(id)
    return redirect(f"/post/{comment.post_id}")
    
@app.route("/comment/<int:id>", methods=["GET", "POST"])
def modifycomment(id):
    comment = comments.get_comment_by_id(id)
    comment = comments.get_comment_by_id(id)
    if (not session["is_admin"]) and comment.owner_id != session["user_id"]:
        return render_template("error.html", 
                                message="Ei sallittu.", 
                                returnUrl="/")
    if request.method == "GET":
        return render_template("modifycomment.html", comment = comment)
    if request.method == "POST":
        content = request.form["content"]
        comments.modify_comment_by_id(id, content)
        return redirect(f"/post/{comment.post_id}")
    
@app.route("/createPrivateTopic", methods=["POST"])
def newprivtopic():
    topic = request.form['topic']
    topics.create_private(topic)
    return redirect("/")

@app.route("/priv_manager")
def priv_manager():
    private_topics = topics.get_accessable_private_topics()
    return render_template("priv_manager.html", pri = private_topics)

@app.route("/priv_manager/<int:id>", methods=["GET", "POST"])
def priv_room_manager(id):
    u = privrooms.get_users_by_privroom_id(id)
    t = topics.get_topic_by_id(id)
    if request.method == "GET":
        return render_template("priv_manager2.html", users = u, topic = t)
    if request.method == "POST":
        username = request.form["username"]
        private_key = request.form["private_key"]
        privrooms.addslip(username, private_key)
        return redirect(f"/priv_manager/{id}")

@app.route("/addpriv/<int:topic_id>", methods=["POST"])
def add_access(topic_id):
    username = request.form["username"]
    try:
        user_id = users.get_user_id_by_name(username)
        privrooms.give_user_access(user_id, topic_id)
        return redirect(f"/priv_manager/{topic_id}")
    except:
        return render_template("error.html", 
                                message="Käyttäjää ei olemassa.", 
                                returnUrl=f"/priv_manager/{topic_id}")

@app.route("/priv_topics")
def privtopics():
    t = topics.get_accessable_private_topics()
    return render_template("priv_topics.html", content = t)

@app.route("/delpriv/<int:user_id>/<int:topic_id>")
def del_access(user_id, topic_id):
    privrooms.delet_user_access(user_id, topic_id)
    return redirect(f"/priv_manager/{topic_id}")
    
@app.route("/search", methods = ["POST"])
def search():
    query = request.form["key"]
    result = topics.get_topics_by_search(query)
    return render_template(f"searchresult.html", content = result)