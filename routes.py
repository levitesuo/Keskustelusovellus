from app import app
from flask import redirect, render_template, request, session, abort
import db_modules.users as users
import db_modules.topics as topics
import db_modules.posts as posts
import db_modules.comments as comments
import db_modules.privrooms as privrooms


@app.route("/")
def index():
    t = topics.get_topics()
    return render_template("index.html", content=t)


@app.route("/notAllowed")
def not_allowed():
    return render_template("error.html",
                           message="Ei sallittu.",
                           returnUrl="/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html",
                                   message="Väärä salasana tai käyttäjä",
                                   returnUrl="/login")
        return redirect("/")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/newuser", methods=["GET", "POST"])
def create_account():
    if request.method == "GET":
        return render_template("newuser.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html",
                                   message="Salasanat eroavat",
                                   returnUrl="/newuser")
        if users.register(username, password1):
            return redirect("/")
        return render_template("error.html",
                               message="Käyttäjänimi varattu.",
                               returnUrl="/newuser")


@app.route("/createTopic", methods=["POST"])
def create_topic():
    if session.get("is_admin"):
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        new_topic = request.form["topic"]
        topics.create(new_topic)
        return redirect("/")
    return redirect("/notAllowed")


@app.route("/topic/delete/<int:topic_id>")
def delete_topic(topic_id):
    if session.get("is_admin"):
        privet_key = topics.get_topic_by_id(id).private_key
        topics.delete_topic_by_id(topic_id)
        if privet_key:
            return redirect("/priv_topics")
        return redirect("/")
    return redirect("/notAllowed")


@app.route("/topic/<int:topic_id>", methods=["GET", "POST"])
def topic_page(topic_id):
    if request.method == "GET":
        topic_content = topics.get_topic_by_id(topic_id)
        posts_content = posts.get_posts_by_topic(topic_id)
        return render_template("topic.html",
                               topic_content=topic_content,
                               posts_content=posts_content)
    if request.method == "POST":
        if session.get("username"):
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            header = request.form["header"]
            content = request.form["content"]
            posts.new_post(topic_id, header, content)
            return redirect(f"/topic/{topic_id}")
        return redirect("/notAllowed")


@app.route("/post/delete/<int:post_id>")
def delete_post(post_id):
    post_to_be_del = posts.get_post_by_id(post_id)
    if session.get("username") and (session["is_admin"] or post_to_be_del.owner_id == session["user_id"]):
        posts.delete_post_by_id(post_id)
        return redirect(f"/topic/{post_to_be_del.topic_id}")
    return redirect("/notAllowed")


@app.route("/post/modify/<int:post_id>", methods=["GET", "POST"])
def modify_post(post_id):
    post_to_be_modified = posts.get_post_by_id(post_id)
    if session.get("username") and (session["is_admin"] or post_to_be_modified.owner_id == session["user_id"]):
        if request.method == "GET":
            return render_template("modifypost.html", post=post_to_be_modified)
        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            header = request.form["header"]
            content = request.form["content"]
            posts.modify_post_by_id(post_id, content, header)
            return redirect(f"/topic/{post_to_be_modified.topic_id}")
    return redirect("/notAllowed")


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def post_page(post_id):
    if request.method == "GET":
        content_post = posts.get_post_by_id(post_id)
        content_comments = comments.get_comments_by_post(post_id)
        return render_template("post.html",
                               content_post=content_post,
                               content_comments=content_comments)
    if request.method == "POST":
        if session.get("username"):
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            content = request.form["content"]
            comments.new_comment(post_id,  content)
            return redirect(f"/post/{post_id}")
        return redirect("/notAllowed")


@app.route("/comment/delete/<int:comt_id>")
def delete_comment(comt_id):
    comt_to_be_del = comments.get_comment_by_id(comt_id)
    if session.get("username") and (session["is_admin"] or comt_to_be_del.owner_id == session["user_id"]):
        comments.delete_comment_by_id(comt_id)
        return redirect(f"/post/{comt_to_be_del.post_id}")
    return redirect("/notAllowed")


@app.route("/comment/<int:comt_id>", methods=["GET", "POST"])
def modify_comment(comt_id):
    comt_to_be_mod = comments.get_comment_by_id(comt_id)
    if session.get("username") and (session["is_admin"] or comt_to_be_mod.owner_id == session["user_id"]):
        if request.method == "GET":
            return render_template("modifycomment.html", comment=comt_to_be_mod)
        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            content = request.form["content"]
            comments.modify_comment_by_id(comt_id, content)
            return redirect(f"/post/{comt_to_be_mod.post_id}")
    return redirect("/notAllowed")


@app.route("/createPrivateTopic", methods=["POST"])
def new_priv_topic():
    if session.get("is_admin") and session["is_admin"]:
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        new_topic = request.form['topic']
        topics.create_private(new_topic)
        return redirect("/")
    return redirect("/notAllowed")


@app.route("/priv_manager")
def priv_manager():
    if session["is_admin"]:
        private_topics = topics.get_accessable_private_topics()
        return render_template("priv_manager.html", pri=private_topics)
    return redirect("/notAllowed")


@app.route("/priv_manager/<int:topic_id>", methods=["GET", "POST"])
def priv_room_manager(topic_id):
    if session.get("is_admin") and session["is_admin"]:
        allowed_users = privrooms.get_users_by_privroom_id(topic_id)
        content_topic = topics.get_topic_by_id(topic_id)
        if request.method == "GET":
            return render_template("priv_manager2.html", users=allowed_users, topic=content_topic)
        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            username = request.form["username"]
            private_key = request.form["private_key"]
            privrooms.give_user_access(username, private_key)
            return redirect(f"/priv_manager/{topic_id}")
    return redirect("/notAllowed")


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
    if session.get("username"):
        t = topics.get_accessable_private_topics()
        return render_template("priv_topics.html", content=t)
    return redirect("/notAllowed")


@app.route("/delpriv/<int:user_id>/<int:topic_id>")
def del_access(user_id, topic_id):
    if session.get("is_admin"):
        privrooms.delet_user_access(user_id, topic_id)
        return redirect(f"/priv_manager/{topic_id}")
    return redirect("/notAllowed")


@app.route("/search", methods=["POST"])
def search():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    query = request.form["key"]
    result = posts.get_posts_by_search(query)
    return render_template("searchresult.html", content=result, query=query)
