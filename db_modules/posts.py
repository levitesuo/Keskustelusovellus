from sqlalchemy.sql import text
from flask import session
from db import db

def get_posts_by_topic(topic_id):
    sql = """   SELECT posts.*, users.username
                FROM posts 
                JOIN users ON posts.owner_id = users.user_id
                WHERE posts.topic_id =:topic_id"""
    result = db.session.execute(text(sql), {'topic_id':topic_id})
    posts = result.fetchall()
    return posts

def new_post(topic_id, header, content):
    sql = """INSERT INTO posts  (topic_id, header, content, owner_id, timestamp) 
             VALUES             (:topic_id, :header, :content, :owner_id, NOW())"""
    db.session.execute(text(sql), {'topic_id':topic_id, 'header':header, 'content':content, 'owner_id':session["user_id"]})
    db.session.commit()
    
def get_post_by_id(id):
    sql = "SELECT * FROM posts WHERE post_id =:id"
    result = db.session.execute(text(sql), {'id':id})
    post = result.fetchone()
    return post

def delete_post_by_id(id):
    sql = "DELETE FROM posts WHERE post_id=:id"
    db.session.execute(text(sql), {'id':id})
    db.session.commit()
    
def modify_post_by_id(id, content, header):
    sql = "UPDATE posts SET content = :content, header = :header WHERE post_id=:id"
    result = db.session.execute(text(sql), {'id':id, 'content':content, 'header':header})
    db.session.commit()