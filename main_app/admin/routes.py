from flask import Blueprint, render_template, request, redirect, url_for
from main_app.roles import role_required
from main_app.models import User, Lectures, LectureRooms, LectureEnrollment
from main_app.extensions import db, bcrypt

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
@role_required('Admin')
def dashboard():
    return render_template('admin/dashboard.html')


# Users
from sqlalchemy import or_

@admin.route('users')
@role_required('Admin')
def users():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')

    query = User.query

    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            or_(
                User.firstName.ilike(search_term),
                User.lastName.ilike(search_term),
                User.email.ilike(search_term)
            )
        )

    users = query.order_by(User.uid).paginate(page=page, per_page=50)
    return render_template('admin/users.html', users=users, search_query=search_query)

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
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')

    query = Lectures.query

    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(Lectures.title.ilike(search_term))

    lectures = query.order_by(Lectures.lid).paginate(page=page, per_page=50)
    return render_template('admin/lectures.html', lectures=lectures, search_query=search_query)

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


# Manage Rooms
@admin.route('lectures/rooms/<int:lid>', methods=['GET', 'POST'])
@role_required('Admin')
def manage_rooms(lid: int):
    lecture = Lectures.query.get_or_404(lid)

    if request.method == 'POST':
        name = request.form.get('name')
        capacity = request.form.get('capacity')

        room = LectureRooms(lecture_id=lid, name=name, capacity=capacity)
        try:
            db.session.add(room)
            db.session.commit()
        except Exception as e:
            return f'ERROR: {e}'

        return redirect(url_for('admin.manage_rooms', lid=lid))

    rooms = LectureRooms.query.filter_by(lecture_id=lid).all()
    enrollments = LectureEnrollment.query.filter_by(lecture_id=lid).all()

    return render_template('admin/manage_rooms.html', lecture=lecture, rooms=rooms, enrollments=enrollments)

@admin.route('lectures/rooms/delete/<int:lrid>')
@role_required('Admin')
def delete_room(lrid: int):
    room = LectureRooms.query.get_or_404(lrid)
    lid = room.lecture_id
    try:
        db.session.delete(room)
        db.session.commit()
    except Exception as e:
        return f'ERROR: {e}'

    return redirect(url_for('admin.manage_rooms', lid=lid))

@admin.route('lectures/assign_rooms/<int:lid>', methods=['POST'])
@role_required('Admin')
def assign_rooms(lid: int):
    rooms = LectureRooms.query.filter_by(lecture_id=lid).order_by(LectureRooms.capacity.desc()).all()
    enrollments = LectureEnrollment.query.filter_by(lecture_id=lid).all()

    if not rooms:
        return "No rooms available for this lecture."

    current_room_idx = 0
    current_room_count = 0

    # Reset all assignments first? Or just overwrite?
    # Let's overwrite.

    for enrollment in enrollments:
        if current_room_idx >= len(rooms):
            # No more rooms available
            enrollment.room_assigned = "Overflow" # or None
        else:
            room = rooms[current_room_idx]
            enrollment.room_assigned = room.name
            current_room_count += 1

            if current_room_count >= room.capacity:
                current_room_idx += 1
                current_room_count = 0

    try:
        db.session.commit()
    except Exception as e:
        return f'ERROR: {e}'

    return redirect(url_for('admin.manage_rooms', lid=lid))
