'''
Custom views for the Flask-Admin interface. Defines access control and custom behavior for:
- MyAdminIndexView: Custom admin dashboard view with access control.
- AuthModelView: Base view with login requirement for accessing models.
- Specific views (UserView, PostView, CommentView, LikeView, ShareView, ReportView): Configure form columns and list columns
for managing respective models and handle custom delete behavior for posts.
'''

from flask import redirect, url_for, flash, session
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

from .models import User, Post
from . import db

# Custom admin dashboard view with access control
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not session.get('logged_in'):
            flash('You are not logged in!', 'error')
            return redirect(url_for('auth.login'))

        total_users, total_posts = db.session.query(User).count(), db.session.query(Post).count()
        return self.render('dashboard.html', total_users=total_users, total_posts=total_posts)

# Base view with login requirement for accessing models
class AuthModelView(ModelView):
    # Function to check if user is logged in
    def is_accessible(self):
        return session.get('logged_in')

    # Function to handle inaccessible views
    def inaccessible_callback(self, name, **kwargs):
        flash('You are not logged in!', 'error')
        return redirect(url_for('auth.login'))

class UserView(AuthModelView):
    form_columns = ["name"]
    column_list = ["name", "created_date", "created_time"]

    # function to format list columns of the User model
    def _list_formatter(view, context, model, name):
        if name == 'created_date':
            return model.created_date
        elif name == 'created_time':
            return model.created_time
        return super(UserView, view)._list_formatter(context, model, name) # Call parent method

class PostView(AuthModelView):
    can_delete = True # Allow deletion of posts
    form_columns = ['user', 'title', 'body']
    column_list = ['user', 'title', 'body', 'comments_count', 'likes_count', 'shares_count', 'reports_count']

    def on_model_delete(self, model):
        if model.user:
            model.user.posts.remove(model)
            db.session.commit()

class CommentView(AuthModelView):
    form_columns = ['user', 'post', 'content']
    column_list = ['user', 'post', 'content']

class LikeView(AuthModelView):
    form_columns = ['user', 'post']
    column_list = ['user', 'post']

class ShareView(AuthModelView):
    form_columns = ['user', 'post']
    column_list = ['user', 'post']

class ReportView(AuthModelView):
    form_columns = ['user', 'post']
    column_list = ['user', 'post']
