from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship('Post')

    # def __repr__(self):
       # return f"User Id('{self.subject}', '{self.content}'"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    content = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_reply = db.Column(db.Boolean, default=False)

    # def __repr__(self):
       # return f"User Id('{self.subject}', '{self.date_posted}'"

    def get_JSON(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "date_posted": self.date_posted.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "user_id": self.user_id,
            "is_reply": self.is_reply
        }
    
    def load_from_JSON(self, json_data):
        self.subject = json_data['subject']
        self.date_posted = datetime.datetime.strptime(json_data['date_posted'], "%Y-%m-%d %H:%M:%S")
        self.content = json_data['content']
        self.user_id = json_data['user_id']
        self.is_reply = json_data['is_reply']
        return self

class Initial_Post(db.Model):
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    is_pulled_once = db.Column(db.Boolean, default=False)

class Responding_Post(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    respond_to = db.Column(db.Integer, db.ForeignKey('post.id'))
    reply = db.Column(db.Integer, db.ForeignKey('post.id'))


letters = [
    {
        'subject': 'example 1',
        'content': 'content 1'
    },
    {
        'subject': 'example 2',
        'content': 'content 2'
    }
]