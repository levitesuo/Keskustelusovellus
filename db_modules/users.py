from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
import secrets
from sqlalchemy.sql import text
from db import db

def get_user_id():
    return session.get("user_id", 0)

def get_user_by_id(id):
    sql = "SELECT * FROM users WHERE user_id =:id"
    result = db.session.execute(text(sql), {'id':id})
    user = result.fetchone()
    return user

def get_user_id_by_name(username):
    sql = "SELECT users.user_id FROM users WHERE username = :username"
    result = db.session.execute(text(sql), {'username':username})
    user_id = int(result.fetchone().user_id)
    return user_id

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
            session["csrf_token"] = secrets.token_hex(16)
            if user.is_admin: 
                session["is_admin"] = True
            else:
                session["is_admin"] = False
            return True
        else:
            return False
        
def register(username, password):
    try:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password);"
        db.session.execute(text(sql), {'username':username, 'password':hash_value,})
        db.session.commit()
    except:
        return False
    return login(username, password)