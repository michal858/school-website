from flask import Blueprint, render_template
from flask_login import current_user
from main_app.roles import role_required


students = Blueprint('students', __name__, template_folder='templates')

@students.route('/')
@role_required('Student')
def dashboard():
    return render_template('students/dashboard.html', current_user=current_user)
