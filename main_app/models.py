from main_app.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50))

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



class LectureEnrollment(db.Model):
    __tablename__ = 'lecture_enrollment'

    leid = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<LectureEnrollment: {self.user_id} {self.lecture_id}>"

    def get_id(self):
        return self.leid
