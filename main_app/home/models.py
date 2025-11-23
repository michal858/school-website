from main_app.extensions import db

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
