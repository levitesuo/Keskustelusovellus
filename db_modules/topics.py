from sqlalchemy.sql import text
from flask import session
from db import db

def get_topics():
    sql = """   SELECT topics.*, users.username, 
                COUNT(posts.post_id) AS post_count,
                MAX(posts.timestamp) AS last_post
                FROM topics 
                JOIN users ON topics.owner_id = users.user_id
                JOIN posts ON topics.topic_id = posts.topic_id
                WHERE private_key IS NULL
                GROUP BY topics.topic_id, users.username"""
    result = db.session.execute(text(sql))
    t = result.fetchall()
    return t    

def get_accessable_private_topics():
    if session["is_admin"]:
        sql = """   SELECT topics.*, users.username, 
                    COUNT(posts.post_id) AS post_count,
                    MAX(posts.timestamp) AS last_post
                    FROM topics 
                    JOIN users ON topics.owner_id = users.user_id
                    JOIN posts ON topics.topic_id = posts.topic_id
                    WHERE private_key IS NOT NULL
                    GROUP BY topics.topic_id, users.username"""
        result = db.session.execute(text(sql))
    else:
        sql = """SELECT t.*, u.username
                FROM topics t
                JOIN privrooms p ON t.private_key = p.private_key
                JOIN users u ON t.owner_id = u.user_id
                WHERE p.user_id = :user_id"""
        result = db.session.execute(text(sql), {'user_id':session['user_id']})
    private_topics = result.fetchall()
    return private_topics
    
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

def get_topics_by_search(key):
    sql = """   SELECT DISTINCT p.*, u.username 
                FROM posts p
                JOIN users u ON p.owner_id = u.user_id
                JOIN topics t ON p.topic_id = t.topic_id
                JOIN privrooms pr ON (
                (t.private_key = pr.private_key 
                AND pr.user_id = :user_id)
                OR t.private_key IS NULL)
                WHERE p.content LIKE :query
                OR p.header LIKE :query"""
    result = db.session.execute(text(sql),{'user_id':session["user_id"], 'query':key})   
    stuff = result.fetchall()
    return stuff
    