from sqlalchemy.sql import text
from flask import session
from db import db

def get_users_by_privroom_id(id):
    sql = """SELECT privrooms.*, users.user_id 
            FROM privrooms 
            JOIN users on privrooms.user_id = users.user_id 
            WHERE privrooms.private_key = :id"""
    result = db.session.execute(text(sql), {'id':id})
    users = result.fetchall()
    return users
