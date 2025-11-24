from flask import Blueprint, render_template, request, redirect, url_for
from main_app.roles import role_required
from main_app.models import User
from main_app.extensions import db

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
@role_required('Admin')
def dashboard():
    return render_template('admin/dashboard.html')



@admin.route('users')
@role_required('Admin')
def users():
    users = User.query.order_by(User.uid).all()
    return render_template('admin/users.html', users=users)


@admin.route('users/<int:uid>/edit', methods=['GET', 'POST'])
@role_required('Admin')
def edit_user(uid:int):
    if request.method == 'GET':
        user = User.query.get_or_404(uid)
        return render_template('admin/edit_user.html', user=user)
    elif request.method == 'POST':
        user = User.query.get_or_404(uid)
        user.firstName = request.form.get('firstName')
        user.lastName = request.form.get('lastName')
        user.email = request.form.get('email')
        user.role = request.form.get('role')

        
        db.session.commit()
        return redirect(url_for('admin.users'))

    else:
        print('Something went wrong')

@admin.route('users/<int:uid>/delete', methods=['POST'])
@role_required('Admin')
def delete_user(uid):
    return render_template('admin/delete_user.html')


