from flask import Blueprint, render_template, request, redirect, url_for
from main_app.roles import role_required
from main_app.models import User, Lectures
from main_app.extensions import db, bcrypt

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
@role_required('Admin')
def dashboard():
    return render_template('admin/dashboard.html')


# Users
@admin.route('users')
@role_required('Admin')
def users():
    users = User.query.order_by(User.uid).all()
    return render_template('admin/users.html', users=users)

# Edit User
@admin.route('users/edit/<int:uid>', methods=['GET', 'POST'])
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
        user.password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        user.role = request.form.get('role')

        try:
            db.session.commit()
            return redirect(url_for('admin.users'))
        except Exception as e:
            return f'ERROR: {e}'

    else:
        return 'Something went wrong'

# Delete User
@admin.route('users/delete/<int:uid>', methods=['POST', 'GET'])
@role_required('Admin')
def delete_user(uid:int):
    user = User.query.get_or_404(uid)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('admin.users'))
    except Exception as e:
        return f'ERROR: {e}'

# Add User
@admin.route('users/add', methods=['POST', 'GET'])
@role_required('Admin')
def add_user():
    if request.method == 'GET':
        return render_template('admin/add_user.html')
    elif request.method == 'POST':
        user = User()
        user.firstName = request.form.get('firstName')
        user.lastName = request.form.get('lastName')
        user.email = request.form.get('email')
        user.role = request.form.get('role')
        user.password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return f'ERROR: {e}'

        return redirect(url_for('admin.users'))




# Lectures
@admin.route('lectures')
@role_required('Admin')
def lectures():
    lectures = Lectures.query.order_by(Lectures.lid).all()
    return render_template('admin/lectures.html', lectures=lectures)

# Edit Lecture
@admin.route('lectures/edit/<int:lid>', methods=['GET', 'POST'])
@role_required('Admin')
def edit_lecture(lid:int):
    if request.method == 'GET':
        lecture = Lectures.query.get_or_404(lid)
        return render_template('admin/edit_lecture.html', lecture=lecture)
    elif request.method == 'POST':
        lecture = Lectures.query.get_or_404(lid)
        lecture.title = request.form.get('title')
        lecture.description = request.form.get('description')
        lecture.teacher_id = request.form.get('teacher_id')

        try:
            db.session.commit()
            return redirect(url_for('admin.lectures'))
        except Exception as e:
            return f'ERROR: {e}'

    else:
        return 'Something went wrong'

# Delete Lecture
@admin.route('lectures/delete/<int:lid>', methods=['POST', 'GET'])
@role_required('Admin')
def delete_lecture(lid:int):
    lecture = Lectures.query.get_or_404(lid)
    try:
        db.session.delete(lecture)
        db.session.commit()
        return redirect(url_for('admin.lectures'))
    except Exception as e:
        return f'ERROR: {e}'

# Add Lecture
@admin.route('lectures/add', methods=['POST', 'GET'])
@role_required('Admin')
def add_lecture():
    if request.method == 'GET':
        return render_template('admin/add_lecture.html')
    elif request.method == 'POST':
        lecture = Lectures()
        lecture.title = request.form.get('title')

        try:
            db.session.add(lecture)
            db.session.commit()
        except Exception as e:
            return f'ERROR: {e}'

        return redirect(url_for('admin.lectures'))
    else:
        return 'Something went wrong'
