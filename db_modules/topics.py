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

def create_private(topic):
    create(topic)
    sql1 = "SELECT MAX(topic_id) AS m FROM topics"
    result = db.session.execute(text(sql1))
    priv_key = int(result.fetchone().m)
    sql = "UPDATE topics SET private_key = :priv_key WHERE topic_id=:priv_key"
    db.session.execute(text(sql),{'priv_key':priv_key})
    db.session.commit()

def get_topic_by_id(id):
    sql = "SELECT * FROM topics WHERE topic_id =:id"
    result = db.session.execute(text(sql), {'id':id})
    topic = result.fetchone()
    return topic

def delete_topic_by_id(id):
    sql = "DELETE FROM topics WHERE topic_id=:id"
    db.session.execute(text(sql), {'id':id})
    db.session.commit()