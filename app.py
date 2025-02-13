from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

### database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wellnest.db'
db = SQLAlchemy(app)

class Clinician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __init__(self, name, username, password, role='Junior'):
        self.name = name
        self.username = username
        self.password = password
        self.role = role

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
