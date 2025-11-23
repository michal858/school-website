from flask import Blueprint, render_template
from flask_login import login_required, current_user


students = Blueprint('students', __name__, template_folder='templates')

@students.route('/dashboard')
@login_required
@role_required('Student')
def dashboard():
    return render_template('students/dashboard.html', current_user=current_user)

