from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from sqlalchemy.sql import text
from db import db

def get_user_id():
    return session.get("user_id", 0)

def get_user_by_id(id):
    sql = "SELECT * FROM users WHERE user_id =:id"
    result = db.session.execute(text(sql), {'id':id})
    user = result.fetchone()
    return user

def logout():
    del session["user_id"]
    del session["username"]
    del session["is_admin"]

def login(username, password):
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {'username':username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user.user_id
            if user.is_admin: 
                session["is_admin"] = True
            else:
                session["is_admin"] = False
            return True
        else:
            return False
        
def register(username, password, is_admin):
    try:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin);"
        db.session.execute(text(sql), {'username':username, 'password':hash_value, 'is_admin':is_admin})
        db.session.commit()
    except:
        return False
    return login(username, password)