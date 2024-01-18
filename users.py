from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from sqlalchemy.sql import text
from db import db

def get_user_id():
    return session.get("user_id", 0)

def logout():
    del session["user_id"]
    del session["username"]

def login(username, password):
    sql = "SELECT user_id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {'username':username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user.user_id
            return True
        else:
            return False
        
def register(username, password):
    try:
        hash_value = generate_password_hash(password)
        sql = f"INSERT INTO users (username, password, is_admin) VALUES (:username, :password, FALSE);"
        db.session.execute(text(sql), {'username':username, 'password':hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)