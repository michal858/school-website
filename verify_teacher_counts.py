import unittest
from main_app.app import create_app
from main_app.extensions import db, bcrypt
from main_app.models import User, Lectures, LectureRooms, LectureEnrollment, Attendance

class TestTeacherAttendance(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config={
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create Teacher
            teacher = User(firstName='Teacher', lastName='User', email='teacher@test.com',
                         password=bcrypt.generate_password_hash('password').decode('utf-8'), role='Teacher')
            db.session.add(teacher)

            # Create Lecture
            lecture = Lectures(title='Test Lecture')
            db.session.add(lecture)
            db.session.commit()
            self.lid = lecture.lid

            # Create Rooms
            aula = LectureRooms(lecture_id=self.lid, name='Aula', capacity=90)
            room69 = LectureRooms(lecture_id=self.lid, name='Room 69', capacity=60)
            db.session.add(aula)
            db.session.add(room69)
            db.session.commit()

            # Create Students and Enroll
            # Student 1 in Aula
            s1 = User(firstName='S1', lastName='T', email='s1@test.com', password='p', role='Student')
            db.session.add(s1)
            db.session.commit()
            e1 = LectureEnrollment(lecture_id=self.lid, user_id=s1.uid, room_assigned='Aula')
            db.session.add(e1)

            # Student 2 in Room 69
            s2 = User(firstName='S2', lastName='T', email='s2@test.com', password='p', role='Student')
            db.session.add(s2)
            db.session.commit()
            e2 = LectureEnrollment(lecture_id=self.lid, user_id=s2.uid, room_assigned='Room 69')
            db.session.add(e2)

            db.session.commit()
            self.s1_uid = s1.uid
            self.s2_uid = s2.uid

    def login(self, email, password):
        return self.client.post('/auth/', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_room_attendance(self):
        with self.app.app_context():
            self.login('teacher@test.com', 'password')

            # 1. Access Attendance without room -> Should see select room page (check for room names and counts)
            resp = self.client.get(f'/teacher/attendance/{self.lid}')
            self.assertIn(b'Aula', resp.data)
            self.assertIn(b'Room 69', resp.data)
            self.assertIn(b'Wybierz Sale', resp.data)

            # Check for counts: Aula has 1 student, Room 69 has 1 student
            # Format is "1 / 90" and "1 / 60"
            self.assertIn(b'1 / 90', resp.data)
            self.assertIn(b'1 / 60', resp.data)

if __name__ == '__main__':
    unittest.main()
