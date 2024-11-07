'''
Application factory for creating and configuring the Flask app instance. Initializes Flask extensions such
as SQLAlchemy and Flask-Admin, and sets up the application context. Also ensures that the database schema is
created and initializes the Flask-Admin interface with custom views.
'''

from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()

def create_app():
    from . import routes, admin_views, models # Importing here to avoid circular imports
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(routes.auth_bp)

    db.init_app(app)

    with app.app_context():
        db.create_all() # Create database schema

        admin = Admin(name='MediaDB', index_view=admin_views.MyAdminIndexView())
        admin.init_app(app)

        admin.add_view(admin_views.UserView(models.User, db.session))
        admin.add_view(admin_views.PostView(models.Post, db.session))
        admin.add_view(admin_views.CommentView(models.Comment, db.session))
        admin.add_view(admin_views.LikeView(models.Like, db.session))
        admin.add_view(admin_views.ShareView(models.Share, db.session))
        admin.add_view(admin_views.ReportView(models.Report, db.session))

    return app
