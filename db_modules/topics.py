from sqlalchemy.sql import text
import secrets
from flask import session
from db import db


def get_topics():
    session["csrf_token"] = secrets.token_hex(16)
    sql = """   SELECT t.*, u.username, 
                COUNT(p.post_id) AS post_count,
                MAX(p.timestamp) AS last_post,
                COALESCE(MAX(p.timestamp), t.timestamp) AS o
                FROM topics t
                JOIN users u ON t.owner_id = u.user_id
                LEFT JOIN posts p ON t.topic_id = p.topic_id
                WHERE t.private_key IS NULL
                GROUP BY t.topic_id, u.username
                ORDER BY o DESC"""
    result = db.session.execute(text(sql))
    t = result.fetchall()
    return t


def get_accessable_private_topics():
    if session["is_admin"]:
        sql = """   SELECT t.*, u.username, 
                    COUNT(p.post_id) AS post_count,
                    MAX(p.timestamp) AS last_post,
                    COALESCE(MAX(p.timestamp), t.timestamp) AS o
                    FROM topics t
                    JOIN users u ON t.owner_id = u.user_id
                    LEFT JOIN posts p ON t.topic_id = p.topic_id
                    WHERE t.private_key IS NOT NULL
                    GROUP BY t.topic_id, u.username
                    ORDER BY o DESC"""
        result = db.session.execute(text(sql))
    else:
        sql = """   SELECT t.*, u.username, 
                    COUNT(p.post_id) AS post_count,
                    MAX(p.timestamp) AS last_post,
                    COALESCE(MAX(p.timestamp), t.timestamp) AS o
                    FROM topics t
                    JOIN users u ON t.owner_id = u.user_id
                    LEFT JOIN posts p ON t.topic_id = p.topic_id
                    JOIN privrooms pr ON t.private_key = pr.private_key
                    WHERE pr.user_id = :user_id
                    GROUP BY t.topic_id, u.username
                    ORDER BY o DESC"""
        result = db.session.execute(text(sql), {'user_id': session['user_id']})
    private_topics = result.fetchall()
    return private_topics


def create(topic):
    sql = "INSERT INTO topics (header, owner_id, timestamp) VALUES (:topic, :owner_id, NOW())"
    db.session.execute(
        text(sql), {'topic': topic, 'owner_id': session["user_id"]})
    db.session.commit()


def create_private(topic):
    create(topic)
    sql1 = "SELECT MAX(topic_id) AS m FROM topics"
    result = db.session.execute(text(sql1))
    priv_key = int(result.fetchone().m)
    sql = "UPDATE topics SET private_key = :priv_key WHERE topic_id=:priv_key"
    db.session.execute(text(sql), {'priv_key': priv_key})
    db.session.commit()


def get_topic_by_id(id):
    sql = "SELECT * FROM topics WHERE topic_id =:id"
    result = db.session.execute(text(sql), {'id': id})
    topic = result.fetchone()
    return topic


def delete_topic_by_id(id):
    sql = "DELETE FROM topics WHERE topic_id=:id"
    db.session.execute(text(sql), {'id': id})
    db.session.commit()


def get_posts_by_search(query):
    key = "%"+query+"%"
    if session.get("user_id"):
        sql = """   SELECT DISTINCT p.*, u.username, t.header AS topic_header
                    FROM posts p
                    JOIN users u ON p.owner_id = u.user_id
                    JOIN topics t ON p.topic_id = t.topic_id
                    JOIN privrooms pr ON (
                    (t.private_key = pr.private_key 
                    AND pr.user_id = :user_id)
                    OR t.private_key IS NULL)
                    WHERE p.content LIKE :query
                    OR p.header LIKE :query
                    ORDER BY p.timestamp DESC"""
        result = db.session.execute(
            text(sql), {'user_id': session["user_id"], 'query': key})
    else:
        sql = """   SELECT DISTINCT p.*, u.username, t.header AS topic_header
                    FROM posts p
                    JOIN users u ON p.owner_id = u.user_id
                    JOIN topics t ON p.topic_id = t.topic_id
                    WHERE (p.content LIKE :query
                    OR p.header LIKE :query) 
                    AND t.private_key IS NULL
                    ORDER BY p.timestamp DESC"""
        result = db.session.execute(text(sql), {'query': key})
    stuff = result.fetchall()
    return stuff
