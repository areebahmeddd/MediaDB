'''
Defines the application routes and their associated handlers for:
- Login: Handles user authentication and session management.
- Signup: Manages the registration of new admin users, including validation and password hashing.
- Logout: Handles user logout by clearing the session and redirecting to the login page.
'''

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from .models import AdminUser, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin_user = AdminUser.query.filter_by(username=username).first()
        if admin_user and check_password_hash(admin_user.password, password):
            session['logged_in'] = True
            session['username'] = admin_user.username
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid credentials!', 'error')
    return render_template('sign_in.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = AdminUser.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists! Please choose a different one.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            admin_user = AdminUser(username=username, password=hashed_password)
            db.session.add(admin_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('sign_up.html')

@auth_bp.route('/logout')
def logout():
    if session.get('logged_in'):
        session.pop('logged_in')
        session.pop('username')
        flash('You have been logged out!', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash('You are not logged in!', 'error')
        return redirect(url_for('auth.login'))
