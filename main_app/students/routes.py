from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from main_app.roles import role_required
from main_app.models import Lectures, LectureEnrollment
from main_app.extensions import db


students = Blueprint('students', __name__, template_folder='templates')

@students.route('/')
@role_required('Student')
def dashboard():
    return render_template('students/dashboard.html', current_user=current_user)


@students.route('/pick_lecture', methods=['GET', 'POST'])
@role_required('Student')
def pick_lecture():
    if request.method == 'GET':
        lectures = Lectures.query.order_by(Lectures.lid).all()
        return render_template('students/pick_lecture.html', lectures=lectures)
    elif request.method == 'POST':

        user_id = current_user.uid
        lecture_id = request.form.get('lecture')

        try:
            db.session.add(LectureEnrollment(user_id=user_id, lecture_id=lecture_id))
            db.session.commit()
            return redirect(url_for('students.enrolled_lectures'))
        except Exception as e:
            return f'ERROR: {e}'

    else:
        return 'Something went wrong'


@students.route('/enrolled_lectures')
@role_required('Student')
def enrolled_lectures():
    enrolled_lectures = LectureEnrollment.query.filter_by(user_id=current_user.uid).all()
    return render_template('students/enrolled_lectures.html', enrolled_lectures=enrolled_lectures)


@students.route('/enrolled_lectures/edit/<int:leid>', methods=['GET', 'POST'])
@role_required('Student')
def edit_enrolled_lecture(leid:int):
    if request.method == 'GET':
        lectures = Lectures.query.order_by(Lectures.lid).all()
        return render_template('students/edit_enrolled_lecture.html', lectures=lectures)
    elif request.method == 'POST':
        lecture_id = request.form.get('lecture')

        enrolled_lecture = LectureEnrollment.query.get_or_404(leid)
        enrolled_lecture.lecture_id = lecture_id

        try:
            db.session.commit()
            return redirect(url_for('students.enrolled_lectures'))
        except Exception as e:
            return f'ERROR: {e}'

    else:
        return 'Something went wrong'
