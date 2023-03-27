from flask import Flask, redirect, url_for, request, abort, session
from datetime import timedelta
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

# Configuration
app = Flask(__name__)
app.secret_key = "appsecretkey"
app.permanent_session_lifetime = timedelta(days=30)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shows.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
isAdmin = True


# Data Models
class Content(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(1000))
    genre = db.Column(db.String(100))

    def __init__(self, title, description, genre):
        self.title = title
        self.description = description
        self.genre = genre


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
    content = Content.query.all()
    return f"The Browse Page for {sessionData} \n {content[0].title}"


@app.route("/yourAccount", methods=["GET", "POST"])
def yourAccount():
    loginIfNoSession()

    sessionData = session["username"]
    return f"The Account Page for {sessionData}"


@app.route('/viewData/<data>')
def viewData(data):
    return f"Your Data: {data}"


@app.route("/admin")
def admin():
    if not isAdmin:
        abort(404)

    return redirect(url_for("param", param="Hello Admin"))


@app.route("/addContent", methods=["GET", "POST"])
def addContent():
    if not isAdmin:
        abort(404)

    loginIfNoSession()

    if request.method == "POST":
        title = request.form["title"]

        foundContent = Content.query.filter_by(title=title).first()
        if foundContent:
            return f"Content with title {title} already exists"

        content = Content(title)
        db.session.add(content)
        db.session.commit()
        return f"Content added: {title}"

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
