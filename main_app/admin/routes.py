from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'Admin':
        return "Access Denied", 403
    return render_template('admin/dashboard.html')

