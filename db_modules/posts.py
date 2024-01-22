from sqlalchemy.sql import text
from flask import session
from db import db


def get_posts_by_topic(topic_id):
    sql = """   SELECT posts.*, users.username
                FROM posts 
                JOIN users ON posts.owner_id = users.user_id
                WHERE posts.topic_id =:topic_id
                ORDER BY posts.timestamp DESC"""
    result = db.session.execute(text(sql), {'topic_id': topic_id})
    posts = result.fetchall()
    return posts


def new_post(topic_id, header, content):
    sql = """INSERT INTO posts  (topic_id, header, content, owner_id, timestamp) 
             VALUES             (:topic_id, :header, :content, :owner_id, NOW())"""
    db.session.execute(text(sql), {'topic_id': topic_id, 'header': header,
                       'content': content, 'owner_id': session["user_id"]})
    db.session.commit()


def get_post_by_id(id):
    sql = "SELECT * FROM posts WHERE post_id =:id"
    result = db.session.execute(text(sql), {'id': id})
    post = result.fetchone()
    return post


def delete_post_by_id(id):
    sql = "DELETE FROM posts WHERE post_id=:id"
    db.session.execute(text(sql), {'id': id})
    db.session.commit()


def modify_post_by_id(id, content, header):
    sql = "UPDATE posts SET content = :content, header = :header WHERE post_id=:id"
    result = db.session.execute(
        text(sql), {'id': id, 'content': content, 'header': header})
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
