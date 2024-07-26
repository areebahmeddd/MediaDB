'''
Data seeding script for populating the database with mock data using the Faker library. This script creates
a number of users, posts, comments, likes, shares, and reports to populate the database with realistic
test data.
'''

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from faker import Faker
from app import create_app, db
from app.models import User, Post, Comment, Like, Share, Report

app = create_app()
fake = Faker()

def create_users(num_users=25):
    names = [fake.name() for _ in range(num_users)]
    users = [User(name=name) for name in names]
    db.session.add_all(users)
    db.session.commit()
    return users

def create_posts(users, num_posts=100):
    titles = [fake.sentence(nb_words=6) for _ in range(num_posts)]
    bodies = [fake.text(max_nb_chars=200) for _ in range(num_posts)]
    posts = [
        Post(title=random.choice(titles), body=random.choice(bodies), user=random.choice(users))
        for _ in range(num_posts)
    ]
    db.session.add_all(posts)
    db.session.commit()
    return posts

def create_comments(posts, users, num_comments=200):
    comments = [
        Comment(user=random.choice(users), post=random.choice(posts), content=fake.text(max_nb_chars=100))
        for _ in range(num_comments)
    ]
    db.session.add_all(comments)
    db.session.commit()

def create_likes(posts, users, num_likes=150):
    likes = [
        Like(user=random.choice(users), post=random.choice(posts))
        for _ in range(num_likes)
    ]
    db.session.add_all(likes)
    db.session.commit()

def create_shares(posts, users, num_shares=100):
    shares = [
        Share(user=random.choice(users), post=random.choice(posts))
        for _ in range(num_shares)
    ]
    db.session.add_all(shares)
    db.session.commit()

def create_reports(posts, users, num_reports=50):
    reports = [
        Report(user=random.choice(users), post=random.choice(posts))
        for _ in range(num_reports)
    ]
    db.session.add_all(reports)
    db.session.commit()

def main():
    with app.app_context():
        db.drop_all() # Clear existing database tables before populating
        db.create_all()

        users = create_users()
        posts = create_posts(users)
        create_likes(posts, users)
        create_comments(posts, users)
        create_shares(posts, users)
        create_reports(posts, users)

        print('Database populated successfully.')

if __name__ == '__main__':
    main()
