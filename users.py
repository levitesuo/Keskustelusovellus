from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db

def login_handler(username, password):
    sql = "SELECT user_id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {'username':username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            return True
        else:
            return False
        
def newuser_handler(username, password):
    try:
        hash_value = generate_password_hash(password)
        sql = f"INSERT INTO users (username, password) VALUES (:username, :password);"
        db.session.execute(text(sql), {'username':username, 'password':hash_value})
        db.session.commit()
    except:
        return False
    return login_handler(username, password)