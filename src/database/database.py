from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# user model
class User(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable =False)
    email = db.Column(db.String(130), nullable =False, unique=True)
    password = db.Column(db.Text(), nullable =False)
    created_at = db.Column(db.DateTime(), default =datetime.now())
    updated_at = db.Column(db.DateTime(), onupdate =datetime.now())
    expense = db.relationship('Expense', backref="user")

# Expense model
class Expense(db.Model):
    expense_id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(50), nullable =False)
    amount = db.Column(db.Float(), nullable =False)
    description = db.Column(db.Text(), nullable =False)
    userId = db.Column(db.Integer(), db.ForeignKey("user.user_id"))
    created_at = db.Column(db.DateTime(), default =datetime.now())
    updated_at = db.Column(db.DateTime(), onupdate =datetime.now())