from flask import Blueprint, render_template
from flask_login import login_required
from main_app.roles import role_required

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/dashboard')
@login_required
@role_required('Admin')
def dashboard():
    return render_template('admin/dashboard.html')
