'''
Script for displaying the contents of the database in a tabular format using the Tabulate library. This
script queries the database for various models and prints their information to the console in a readable
grid format. (Use for debugging and testing purposes)
'''

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from tabulate import tabulate
from app.models import User, Post, Comment, Like, Share, Report

app = create_app()

def print_users():
    users = User.query.all()
    table = [[user.name] for user in users]
    print('Users:')
    print(tabulate(table, headers=['Name'], tablefmt='grid'))
    print()

def print_posts():
    posts = Post.query.all()
    table = [[post.user.name, post.title, post.body] for post in posts]
    print('Posts:')
    print(tabulate(table, headers=['User', 'Title', 'Body'], tablefmt='grid'))
    print()

def print_comments():
    comments = Comment.query.all()
    table = [[comment.user.name, comment.post.title, comment.content] for comment in comments]
    print('Comments:')
    print(tabulate(table, headers=['User', 'Post', 'Content'], tablefmt='grid'))
    print()

def print_likes():
    likes = Like.query.all()
    table = [[like.user.name, like.post.title] for like in likes]
    print('Likes:')
    print(tabulate(table, headers=['User', 'Post'], tablefmt='grid'))
    print()

def print_shares():
    shares = Share.query.all()
    table = [[share.user.name, share.post.title] for share in shares]
    print('Shares:')
    print(tabulate(table, headers=['User', 'Post'], tablefmt='grid'))
    print()

def print_reports():
    reports = Report.query.all()
    table = [[report.user.name, report.post.title] for report in reports]
    print('Reports:')
    print(tabulate(table, headers=['User', 'Post'], tablefmt='grid'))
    print()

def main():
    with app.app_context():
        print_users()
        print_posts()
        print_comments()
        print_likes()
        print_shares()
        print_reports()

if __name__ == '__main__':
    main()
