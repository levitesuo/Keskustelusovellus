from sqlalchemy.sql import text
from flask import session
from db import db

def get_users_by_privroom_id(id):
    sql = """SELECT privrooms.*, users.* 
            FROM privrooms 
            JOIN users on privrooms.user_id = users.user_id 
            WHERE privrooms.private_key = :id"""
    result = db.session.execute(text(sql), {'id':id})
    users = result.fetchall()
    return users

def delet_user_access(user_id, topic_id):
                sql = """DELETE FROM privrooms WHERE user_id = :user_id AND private_key = :topic_id"""
                db.session.execute(text(sql), {'user_id':user_id, 'topic_id':topic_id})
                db.session.commit()
                
        
def give_user_access(user_id, topic_id):
        try:
                sql = """INSERT INTO privrooms (user_id, private_key, timestamp) VALUES (:user_id,:topic_id, NOW())"""
                db.session.execute(text(sql), {'user_id':user_id, 'topic_id':topic_id})
                db.session.commit()
                return True
        except:
                return False
