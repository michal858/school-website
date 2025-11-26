from main_app.app import create_app
from main_app.extensions import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created!")
