from flask import Blueprint, render_template, url_for
from flask_login import login_required
from main_app.extensions import db
from main_app.models import Lectures, LectureEnrollment, User
from main_app.roles import role_required

teacher = Blueprint('teacher', __name__, template_folder='templates')

@teacher.route('/dashboard')
@login_required
@role_required('Teacher')
def dashboard():
    lectures = db.session.query(Lectures).all()
    return render_template('teacher/dashboard.html', lectures=lectures)


@teacher.route('/<int:lecture_id>/attendance')
@login_required
@role_required('Teacher')
def attendance(lecture_id):
    lecture = Lectures.query.get_or_404(lecture_id)

    # Query students enrolled in this lecture
    enrolled_students = db.session.query(User)\
        .join(LectureEnrollment, User.uid == LectureEnrollment.user_id)\
        .filter(LectureEnrollment.lecture_id == lecture_id)\
        .all()

    return render_template('teacher/attendance.html', lecture=lecture, enrolled_students=enrolled_students)
