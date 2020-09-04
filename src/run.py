"""Docstring"""
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request, session, flash
import platform

app = Flask(__name__)

app.secret_key = "dung"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)


class User(db.Model):
    """Docstring"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    image_file = db.Column(
        db.String(20),
        nullable=False,
        default='default.jpg'
    )
    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Post(db.Model):
    """Docstring"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False,
        default=datetime.utcnow
    )
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    def __init__(self, title, date_posted, content, user_id):
        self.title = title
        self.date_posted = date_posted
        self.content = content
        self.user_id = user_id


POSTS = [
    {
        'author': "DO Manh Dung",
        'date': "20/08/2020",
        'content': "check content 1",
        'title': "check it out 1"
    },
    {
        'author': "DO Manh Hung",
        'date': "19/08/2020",
        'content': "check content 2",
        'title': "check it out 2"
    }
]


@app.route('/')
def hello_world():
    """Docstring"""
    return render_template('home.html', posts=POSTS)


@app.route('/login', methods=["POST", "GET"])
def login():
    """Docstring"""
    if request.method == "POST":
        session.permanent = True
        email = request.form["email"]
        found_user = User.query.filter_by(email=email).first()
        if found_user:
            session["username"] = found_user.username
            session["email"] = found_user.email
            session["id"] = found_user.id
            return redirect(url_for("user", user_id=found_user.id))
        else:
            return render_template("login.html")
    else:
        if "email" in session:
            found_user = User.query.filter_by(email=email).first()
            return redirect(url_for("user", user_id=found_user.id))
        return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Docstring"""
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        found_user = User.query.filter_by(email=email).first()
        if found_user:
            flash("your email has been used")
            return redirect("signup")
        else:
            usr = User(username, password, email)
            db.session.add(usr)
            db.session.commit()
            flash("Signup successfully")
        return redirect(url_for('login'))
    else:
        return render_template("signup.html")


@app.route('/user/<user_id>')
def user(user_id):
    """Docstring"""
    if id:
        found_user = User.query.filter_by(id=user_id).first()
        return render_template("user.html", user=found_user)
    return redirect(url_for("login"))


@app.route("/userlist")
def user_list():
    """Docstring"""
    userlist = User.query.filter_by().all()
    return render_template("userlist.html", userlist=userlist)

@app.route("/os")
def os_name():
    """Docstring"""
    return (str(os.template))

    
@app.route('/logout')
def logout():
    """Docstring"""
    session.pop("email",None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    db.create_all()
    app.run(host='172.31.26.206', debug=True)
