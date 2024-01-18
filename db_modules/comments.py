from sqlalchemy.sql import text
from flask import session
from db import db

def get_comments_by_post(post_id):
    sql = """   SELECT comments.*, users.username
                FROM comments 
                JOIN users ON comments.owner_id = users.user_id
                WHERE comments.post_id =:post_id"""
    result = db.session.execute(text(sql), {'post_id':post_id})
    comments = result.fetchall()
    return comments

def new_comment(post_id, content):
    sql = """INSERT INTO comments (post_id, content, owner_id, timestamp) 
             VALUES             (:post_id, :content, :owner_id, NOW())"""
    db.session.execute(text(sql), {'post_id':post_id, 'content':content, 'owner_id':session["user_id"]})
    db.session.commit()