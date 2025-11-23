from flask import Blueprint, render_template, url_for
from flask_login import current_user, login_required
from main_app.extensions import db

teacher = Blueprint('teacher', __name__, template_folder='templates')

@teacher.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'Teacher':
        return "Access Denied", 403
    return render_template('teacher/dashboard.html')
