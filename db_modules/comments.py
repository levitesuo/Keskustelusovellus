from sqlalchemy.sql import text
from flask import session
from db import db


def get_comments_by_post(post_id):
    sql = """   SELECT comments.*, users.username
                FROM comments 
                JOIN users ON comments.owner_id = users.user_id
                WHERE comments.post_id =:post_id
                ORDER BY comments.timestamp DESC"""
    result = db.session.execute(text(sql), {'post_id': post_id})
    comments = result.fetchall()
    return comments


def new_comment(post_id, content):
    sql = """   INSERT INTO comments    (post_id, content, owner_id, timestamp) 
                VALUES                  (:post_id, :content, :owner_id, NOW())"""
    db.session.execute(text(
        sql), {'post_id': post_id, 'content': content, 'owner_id': session["user_id"]})
    db.session.commit()


def delete_comment_by_id(id):
    sql = "DELETE FROM comments WHERE comment_id=:id"
    db.session.execute(text(sql), {'id': id})
    db.session.commit()


def get_comment_by_id(id):
    sql = "SELECT * FROM comments WHERE comment_id =:id"
    result = db.session.execute(text(sql), {'id': id})
    comment = result.fetchone()
    return comment


def modify_comment_by_id(id, content):
    sql = "UPDATE comments SET content = :content WHERE comment_id=:id"
    result = db.session.execute(text(sql), {'id': id, 'content': content})
    db.session.commit()
