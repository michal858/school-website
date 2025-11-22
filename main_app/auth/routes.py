from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from main_app.extensions import db, bcrypt
from .models import User

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('home.index'))
        return render_template('auth/login')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home.index'))
        else:
            return "Wrong Email or Password"
    else:
        return "Something went wrong"


@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('home.index'))
        return render_template('auth/signup.html')
    elif request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            return "User with that email already exists."

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(firstName=firstName, lastName=lastName, password=hashed_password, email=email)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('home.index'))

    return "Somthing went wrong"

@auth.route('/forgot_password')
def forgot_password():
    return "Forgot password"


@auth.logout('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
