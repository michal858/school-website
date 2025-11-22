from main_app.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=True)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    role = db.Column(db.String(50))

    def __repr__(self):
        return f"<User: {self.firstName} {self.lastName}, Email: {self.email}>"

    def get_id(self):
        return self.uid
