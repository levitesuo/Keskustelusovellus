from sqlalchemy.sql import text
from db import db

def create(topic):
    sql = "INSERT INTO topics (header) VALUES (:topic)"
    db.session.execute(text(sql), {'topic':topic})
    db.session.commit()