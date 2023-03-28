from flask import Flask, redirect, url_for, request, abort, session, jsonify
from datetime import timedelta, datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Configuration
app = Flask(__name__)
app.secret_key = "appsecretkey"
app.permanent_session_lifetime = timedelta(days=30)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app-db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
isAdmin = True


# Data Models
watched = db.Table('watched',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                   db.Column('content_id', db.Integer, db.ForeignKey('content.id')))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    watchHistory = db.relationship(
        "Content", secondary=watched, backref=db.backref('watchers', lazy='dynamic'))

    @property
    def password(self):
        raise AttributeError("Password is not-readable")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, name, email,  password):
        self.name = name
        self.email = email
        self.password = password


def __getUser(user_id):
    return User.query.filter_by(id=user_id).first()


class Content(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000))
    genre = db.Column(db.String(100))

    def __init__(self, title, description, genre):
        self.title = title
        self.description = description
        self.genre = genre


def __getContent(content_id):
    return Content.query.filter_by(id=content_id).first()


# Routes
@app.route('/')
def index():
    return redirect(url_for("login"))


@app.route("/createUser", methods=["POST"])
def createUser():
    email = request.form["email"]
    foundUser = User.query.filter_by(email=email).first()
    if foundUser:
        return f"User already registered with that email"

    name = request.form["name"]
    password = request.form["password"]

    user = User(name, email, password)
    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id

    return redirect(url_for("browse"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        foundUser = User.query.filter_by(email=email).first()

        if not foundUser.verify_password(password):
            return f"Invalid email or password"

        session.permanent = True
        session["user_id"] = foundUser.id
        return redirect(url_for("browse"))

    elif "user_id" in session:
        return redirect(url_for("browse"))

    return "The Login Page"


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/browse")
def browse():
    loginIfNoSession()

    user = __getUser(session["user_id"])
    contentData = Content.query.all()

    feed = []
    for c in contentData:
        content_data = {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "genre": c.genre,
        }
        feed.append(content_data)

    return f"The Browse Page for {user.name} \n{feed}"


@app.route("/contentDetails")
def contentDetails():
    loginIfNoSession()

    content_id = request.args.get("content_id")
    content = __getContent(content_id)

    contentDetails = {
        "title": content.title,
        "description": content.description,
        "genre": content.genre,
    }

    return f"Detail Page for {contentDetails}"


@app.route("/watch")
def watch():
    loginIfNoSession()
    user = __getUser(session["user_id"])
    content_id = request.args.get("content_id")
    content = __getContent(content_id)

    if content not in user.watchHistory:
        user.watchHistory.append(content)
        db.session.commit()
        return f"Added {content.title} to your watch history"

    return f"{content.title} in {user.name}'s watch history", 200


@app.route("/yourAccount", methods=["GET"])
def yourAccount():
    loginIfNoSession()

    user = __getUser(session["user_id"])
    details = [user.name, user.email]

    return f"The Account Page for {user.name}\n{details}"


# Reminder for using params
@app.route('/viewData/<data>')
def viewData(data):
    return f"Your Data: {data}"
    # redirect(url_for("param", param="Hello Admin"))


# Admin Protected Endpoints
@app.route("/admin")
def admin():
    if not isAdmin:
        abort(404)

    return f"Hello Admin"


@app.route("/addContent", methods=["GET", "POST"])
def addContent():
    if not isAdmin:
        abort(404)

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        genre = request.form["genre"]

        content = Content(title, description, genre)
        db.session.add(content)
        db.session.commit()
        return f"Content added: {content}"

    return f"The Add Content Page"


@app.route("/updateContent", methods=["PUT"])
def updateContent():
    if not isAdmin:
        abort(404)

    if request.method == "PUT":
        content_id = request.form["content_id"]
        foundContent = __getContent(content_id)
        if not foundContent:
            return f"Content with id {content_id} not found"

        foundContent.title = request.form["title"]
        foundContent.description = request.form["description"]
        foundContent.genre = request.form["genre"]

        db.session.commit()
        return f"Content updated: {foundContent}"

    return f"The Add Content Page"


@app.route("/viewUsers")
def viewUsers():
    usersData = User.query.all()

    result = []
    for u in usersData:
        user = {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "watchHistory": u.watchHistory,
        }
        result.append(user)

    return f"Users:\n{result}"


# Helper Functions
def loginIfNoSession():
    if "user_id" not in session:
        return redirect(url_for("login"))


# Run App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
