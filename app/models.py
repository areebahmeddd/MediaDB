'''
Defines SQLAlchemy ORM models for the application, including:
- AdminUser: Represents admin users with authentication credentials.
- User: Represents regular users with relationships to posts, comments, likes, shares, and reports.
- Post: Represents user-generated content with associated relationships and properties for counting interactions.
- Comment, Like, Share, Report: Represent user interactions with posts, including comments, likes, shares, and reports.
'''

from . import db
from datetime import datetime

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now())

    posts = db.relationship('Post', back_populates='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')
    likes = db.relationship('Like', back_populates='user', cascade='all, delete-orphan')
    shares = db.relationship('Share', back_populates='user', cascade='all, delete-orphan')
    reports = db.relationship('Report', back_populates='user', cascade='all, delete-orphan')

    def __str__(self):
        return self.name

    @property
    def created_date(self):
        return self.created_at.strftime('%d %B %Y')

    @property
    def created_time(self):
        return self.created_at.strftime('%I:%M %p')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    likes = db.relationship('Like', back_populates='post', cascade='all, delete-orphan')
    shares = db.relationship('Share', back_populates='post', cascade='all, delete-orphan')
    reports = db.relationship('Report', back_populates='post', cascade='all, delete-orphan')

    def __str__(self):
        return self.title

    @property
    def comments_count(self):
        return len(self.comments)

    @property
    def likes_count(self):
        return len(self.likes)

    @property
    def shares_count(self):
        return len(self.shares)

    @property
    def reports_count(self):
        return len(self.reports)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', back_populates='likes')
    post = db.relationship('Post', back_populates='likes')

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', back_populates='shares')
    post = db.relationship('Post', back_populates='shares')

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', back_populates='reports')
    post = db.relationship('Post', back_populates='reports')
