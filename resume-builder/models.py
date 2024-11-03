from db import db  # Import the db instance from db.py

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    objective = db.Column(db.Text, nullable=True)
    education = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Resume {self.name}>'
