from flask.globals import request
from flask import Blueprint, render_template, url_for, redirect
from main_app.extensions import db
from sqlalchemy import func
from main_app.models import Lectures, LectureEnrollment, User, Attendance, LectureRooms
from main_app.roles import role_required

teacher = Blueprint('teacher', __name__, template_folder='templates')

@teacher.route('/')
@role_required('Teacher')
def dashboard():
    # lectures = db.session.query(Lectures).all()
    return render_template('teacher/dashboard.html')



@teacher.route('/lectures')
@role_required('Teacher')
def lectures():
    lectures = db.session.query(Lectures).order_by(Lectures.lid).all()
    return render_template('teacher/lectures.html', lectures=lectures)



@teacher.route('/attendance/<int:lecture_id>', methods=['GET', 'POST'])
@role_required('Teacher')
def attendance(lecture_id):
    lecture = Lectures.query.filter_by(lid=lecture_id).first_or_404()
    rooms = LectureRooms.query.filter_by(lecture_id=lecture_id).all()

    # If rooms exist and no room selected, show room selection
    room_name = request.args.get('room')
    if rooms and not room_name:
        # Calculate counts
        room_counts = {}
        counts = db.session.query(LectureEnrollment.room_assigned, func.count(LectureEnrollment.user_id))\
            .filter_by(lecture_id=lecture_id)\
            .group_by(LectureEnrollment.room_assigned).all()

        for r_name, count in counts:
            room_counts[r_name] = count

        return render_template('teacher/select_room.html', lecture=lecture, rooms=rooms, room_counts=room_counts)

    if request.method == 'POST':
        for key, value in request.form.items():
            if key.startswith('attendance_'):
                user_id = key.split('_')[1]
                attendance_status = value

                # Check if attendance record already exists
                attendance = Attendance.query.filter_by(lecture_id=lecture_id, user_id=user_id).first()

                if attendance:
                    attendance.attendance = attendance_status
                else:
                    attendance = Attendance(lecture_id=lecture_id, user_id=user_id, attendance=attendance_status)
                    db.session.add(attendance)

        db.session.commit()
        # Redirect back to the same room view if applicable
        if room_name:
             return redirect(url_for('teacher.attendance', lecture_id=lecture_id, room=room_name))
        return redirect(url_for('teacher.lectures'))

    elif request.method == 'GET':
        # Query students enrolled in this lecture
        query = db.session.query(User)\
            .join(LectureEnrollment, User.uid == LectureEnrollment.user_id)\
            .filter(LectureEnrollment.lecture_id == lecture_id)

        if room_name:
            query = query.filter(LectureEnrollment.room_assigned == room_name)

        enrolled_students = query.all()

        # Query existing attendance
        attendance_records = Attendance.query.filter_by(lecture_id=lecture_id).all()
        attendance_map = {record.user_id: record.attendance for record in attendance_records}

        return render_template('teacher/attendance.html', lecture=lecture, enrolled_students=enrolled_students, attendance_map=attendance_map, room_name=room_name)
