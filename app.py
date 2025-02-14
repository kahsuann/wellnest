from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
# session
app.secret_key = "wellnest"
app.permanent_session_lifetime = timedelta(minutes=5)
# password hashing
bcrypt = Bcrypt(app)
# database
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
        self.password = bcrypt.generate_password_hash(password)
        self.role = role

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

@app.before_request
def initialise_database():
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

### clinician system

# register
@app.route('/register', methods=['POST'])
def register():
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    if Clinician.query.filter_by(username=username).first():
        return f'{username} is not available, please choose another username.'
    user = Clinician(name=name, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return f'Dr. {user.name} registered successfully. Please login to use WellNest Portal.'

# login
@app.route('/login', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = Clinician.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        session.permanent = True
        session["user"] = username
        return f'Welcome Dr. {user.name}, role: {user.role}'
    return 'Login unsuccessful. Please try again.'

# logout
@app.route('/logout', methods=['POST'])
def logout():
    if "user" in session:
        session.pop("user", None)
    return 'Logout successful. Have a good day!'
    
# promote
@app.route('/promote', methods=['POST'])
def promote():
    username = request.form["username"]
    password = request.form["password"]
    user = Clinician.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        if user.role == 'Senior':
            return f'Dr. {user.name} is already Senior.'
        user.role = 'Senior'
        db.session.commit()
        return f'Dr. {user.name} successfully promoted to Senior.'
    return 'Invalid user details, please try again.'

# demote
@app.route('/demote', methods=['POST'])
def demote():
    username = request.form["username"]
    password = request.form["password"]
    user = Clinician.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        if user.role == 'Junior':
            return f'Dr. {user.name} is already Junior.'
        user.role = 'Junior'
        db.session.commit()
        return f'Dr. {user.name} successfully demoted to Junior.'
    return 'Invalid user details, please try again.'

### therapy cases

# fetch the list of all cases
@app.route('/cases', methods=['GET'])
def cases():
    if "user" in session:
        cases = Case.query.all()
        return jsonify([{'name': case.name, 'description': case.description} for case in cases])
    else:
        return 'Please first log in to view therapy cases.'

# add a case
@app.route('/case', methods=['POST'])
def case():
    if "user" in session:
        name = request.form["name"]
        description = request.form["description"]
        new_case = Case(name=name, description=description)
        db.session.add(new_case)
        db.session.commit()
        return f'New case added successfully. {new_case.name}: {new_case.description}'
    else:
        return 'Please first log in to add a new therapy case.'

if __name__ == '__main__':
    app.run()
