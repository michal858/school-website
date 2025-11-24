from flask import Flask
from dotenv import load_dotenv
import os
from .extensions import db, bcrypt, login_manager, migrate


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST")

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = secret_key


    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'

    from main_app.models import User
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(int(uid))

    from main_app.auth.routes import auth
    from main_app.home.routes import home
    from main_app.admin.routes import admin
    from main_app.teacher.routes import teacher
    from main_app.students.routes import students

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(teacher, url_prefix='/teacher')
    app.register_blueprint(students, url_prefix='/student')



    return app
