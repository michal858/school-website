from main_app.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='Student')

    def __repr__(self):
        return f"<User: {self.firstName} {self.lastName}, Email: {self.email}>"

    def get_id(self):
        return self.uid


class Lectures(db.Model):
    __tablename__ = 'lectures'

    lid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f"<Lecture: {self.title}>"

    def get_id(self):
        return self.lid



    def get_id(self):
        return self.leid


class LectureRooms(db.Model):
    __tablename__ = 'lecture_rooms'

    lrid = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.lid'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    lecture = db.relationship('Lectures', backref='rooms')

    def __repr__(self):
        return f"<LectureRoom: {self.name} ({self.capacity})>"


class LectureEnrollment(db.Model):
    __tablename__ = 'lecture_enrollment'

    leid = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.lid'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    room_assigned = db.Column(db.String(100), nullable=True)

    # Relationship to access the lecture details
    lecture = db.relationship('Lectures', backref='enrollments')

    def __repr__(self):
        return f"<LectureEnrollment: {self.user_id} {self.lecture_id}>"

    def get_id(self):
        return self.leid


class Attendance(db.Model):
    __tablename__ = 'attendance'

    aid = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.lid'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    attendance = db.Column(db.String(50), nullable=False, default='obecny')

    # Relationship to access the lecture details
    lecture = db.relationship('Lectures', backref='attendance')

    def __repr__(self):
        return f"<Attendance: {self.user_id} {self.lecture_id}>"

    def get_id(self):
        return self.aid
