from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

### database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wellnest.db'
db = SQLAlchemy(app)

class Clinician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)

    def __init__(self, name, username, password, role='Junior'):
        self.name = name
        self.username = username
        self.password = password
        self.role = role

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

@app.before_request
def create_tables():
    db.create_all()
    # register clinicians
    if not Clinician.query.first():
        db.session.add_all([
            Clinician(name='Joel Tan',
                    username='joel87',
                    password='pwjoel87',
                    role='Senior'),
            Clinician(name='Huang Shimin',
                    username='shiminh',
                    password='pwshiminh'),
            Clinician(name='Rishi Agarwal',
                    username='rishiaw',
                    password='pwrishiaw')
        ])
    
    # register cases
    if not Case.query.first():
        db.session.add_all([
            Case(name='Jonathan Lim',
                description='A 28-year-old software engineer who is experiencing intense anxiety during team meetings and is struggling to speak up, fearing judgment from colleagues.'),
            Case(name='Angela Paolo',
                 description='A 42-year-old teacher who is coping with the recent loss of a parent and is finding it difficult to concentrate on work and daily responsibilities.'),
            Case(name='Xu Yaoming',
                 description='A 16-year-old high school student who is feeling overwhelmed by academic pressure and is struggling to balance schoolwork, extracurriculars, and personal time.')
        ])
    
    db.session.commit()

if __name__ == '__main__':
    app.run()
