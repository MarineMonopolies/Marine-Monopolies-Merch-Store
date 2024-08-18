import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

basedir = os.path.abspath(os.path.dirname(__file__))

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'web-test.db')
    app.config['SECRET_KEY'] = '899f7a4e08bf49178120f856338d3983'

    
    db.init_app(app)
    Bootstrap(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # No idea what this does
    login_manager.init_app(app)

    from .models import User # Needs to be imported after db is initialized

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
