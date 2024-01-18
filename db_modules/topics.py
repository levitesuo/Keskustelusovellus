from sqlalchemy.sql import text
from flask import session
from db import db

def get_topics():
    sql = """   SELECT topics.*, users.username
                FROM topics
                JOIN users ON topics.owner_id = users.user_id"""
    result = db.session.execute(text(sql))
    t = result.fetchall()
    return t    

def create(topic):
    sql = "INSERT INTO topics (header, owner_id, timestamp) VALUES (:topic, :owner_id, NOW())"
    db.session.execute(text(sql), {'topic':topic, 'owner_id':session["user_id"]})
    db.session.commit()

def get_topic_by_id(id):
    sql = "SELECT * FROM topics WHERE topic_id =:id"
    result = db.session.execute(text(sql), {'id':id})
    topic = result.fetchone()
    return topic