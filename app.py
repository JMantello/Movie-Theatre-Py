from flask import Flask, redirect, url_for, request, abort, session, jsonify
from datetime import timedelta, datetime
from enum import Enum
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
class Content(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(1000))
    genre = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, description, genre):
        self.title = title
        self.description = description
        self.genre = genre


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    watchHistory = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, watchHistory):
        self.username = username
        self.email = email
        self.watchHistory = watchHistory


# Routes
@app.route('/')
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]
        session["username"] = f"{username}'s session"
        return redirect(url_for("browse"))

    elif "username" in session:
        return redirect(url_for("browse"))

    return "The Login Page"


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/browse")
def browse():
    loginIfNoSession()

    sessionData = session["username"]
    contentData = Content.query.all()

    content = []
    for c in contentData:
        content_data = {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "genre": c.genre,
        }
        content.append(content_data)

    return f"The Browse Page for {sessionData} \n{content}"


@app.route("/yourAccount", methods=["GET", "POST"])
def yourAccount():
    loginIfNoSession()

    sessionData = session["username"]
    return f"The Account Page for {sessionData}"


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

        foundContent = Content.query.filter_by(title=title).first()
        if foundContent:
            return f"Content with title {title} already exists"

        content = Content(title, description, genre)
        db.session.add(content)
        db.session.commit()
        return f"Content added: {content}"

    return f"The Add Content Page"


@app.route("/updateContent", methods=["GET", "POST"])
def updateContent():
    if not isAdmin:
        abort(404)

    if request.method == "POST":
        id = request.form["id"]
        foundContent = Content.query.filter_by(id=id).first()
        if not foundContent:
            return f"Content with id {id} not found"

        foundContent.title = request.form["title"]
        foundContent.description = request.form["description"]
        foundContent.genre = request.form["genre"]

        db.session.commit()
        return f"Content updated: {foundContent}"

    return f"The Add Content Page"


# Helper Functions
def loginIfNoSession():
    if "username" not in session:
        return redirect(url_for("login"))


# Run App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
