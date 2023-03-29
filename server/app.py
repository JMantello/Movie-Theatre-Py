from flask import Flask, redirect, url_for, request, abort, session, jsonify, make_response
from datetime import timedelta, datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from faker import Faker
from flask_cors import CORS

# Configuration
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
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


class Content(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000))
    genre = db.Column(db.String(100))
    image_url = db.Column(db.String(400))

    def __init__(self, title, description, genre, image_url):
        self.title = title
        self.description = description
        self.genre = genre
        self.image_url = image_url


def __getContent(content_id):
    return Content.query.filter_by(id=content_id).first()


class ContentSchema(SQLAlchemySchema):
    class Meta:
        model = Content
        load_instance = True

    id = auto_field()
    title = auto_field()
    description = auto_field()
    genre = auto_field()
    image_url = auto_field()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False, nullable=False)
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

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = auto_field()
    name = auto_field()
    email = auto_field()
    isAdmin = auto_field()
    watchHistory = auto_field()


def __getUser(user_id):
    return User.query.filter_by(id=user_id).first()


# Routes
@app.route('/dataSeed')
def dataSeed():
    genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi']
    fake = Faker()

    for i in range(50):
        content = Content(fake.sentence(), fake.text(),
                          fake.random_element(genres), fake.image_url(width=1920, height=1080))

        db.session.add(content)
        db.session.commit()

    for i in range(50):
        user = User(fake.name(), fake.email(), fake.password())

        # Create 3 initial admins
        if i < 3:
            user.isAdmin = True

        # Add 3 random Content to Users 3 - 40(ish) watch history
        contentData = Content.query.all()
        if i > 3 and i < 40:
            for j in range(3):
                user.watchHistory.append(fake.random_element(contentData))

        db.session.add(user)

    db.session.commit()
    return f"Database seeded"


@app.route('/')
def index():
    # session.pop("user_id", None)
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
        foundUser = User.query.filter_by(email=email).first()
        if not foundUser:
            return f"No user found with that email"

        password = request.form["password"]
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
    session.clear()
    return redirect(url_for("login"))


@app.route("/browse")
def browse():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = __getUser(session["user_id"])
    contentData = Content.query.all()

    cs = ContentSchema()

    feed = []
    for c in contentData:
        feed.append(cs.dump(c))

    return f"The Browse Page for {user.name} \n{feed}"


@app.route("/contentDetails")
def contentDetails():
    if "user_id" not in session:
        return redirect(url_for("login"))

    content_id = request.args.get("content_id")
    content = __getContent(content_id)

    if not content:
        return f"Content with content_id: {content_id} was not found"

    cs = ContentSchema()
    contentDetails = cs.dump(content)

    return f"Detail Page for {contentDetails}"


@app.route("/watch")
def watch():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = __getUser(session["user_id"])
    content_id = request.args.get("content_id")
    content = __getContent(content_id)

    if not content:
        return f"Content with content_id: {content_id} was not found"

    if content not in user.watchHistory:
        user.watchHistory.append(content)
        db.session.commit()
        return f"Added {content.title} to your watch history"

    return f"{content.title} in {user.name}'s watch history", 200


@app.route("/yourAccount", methods=["GET"])
def yourAccount():
    if "user_id" not in session:
        return redirect(url_for("login"))

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
        image_url = request.form["image_url"]

        content = Content(title, description, genre, image_url)
        db.session.add(content)
        db.session.commit()
        return f"Content added: {content}"

    return f"The Add Content Page"


@app.route("/updateContent", methods=["GET", "PUT"])
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

    return f"The Update Content Page"


@app.route("/deleteContent", methods=["GET", "DELETE"])
def deleteContent():
    if not isAdmin:
        abort(404)

    if request.method == "DELETE":
        content_id = request.form["content_id"]
        foundContent = __getContent(content_id)
        if not foundContent:
            return f"Content with id {content_id} not found"

        db.session.delete(foundContent)
        db.session.commit()
        return f"Content deleted: {foundContent}"

    return f"The Delete Content Page"


@app.route("/viewUser")
def viewUser():
    user_id = request.args.get("user_id")
    user = __getUser(user_id)

    return f"User:\n{UserSchema().dump(user)}"


@app.route("/viewUsers")
def viewUsers():
    if not isAdmin:
        abort(404)

    us = UserSchema()
    usersData = User.query.all()

    result = []
    for u in usersData:
        result.append(us.dump(u))

    return f"Users:\n{result}"


@app.route("/updateUser", methods=["PUT"])
def updateUser():
    if request.method == "PUT":
        user_id = request.form["user_id"]
        if not user_id == session["user_id"] and not isAdmin:
            abort(404)

        foundUser = __getUser(user_id)
        if not foundUser:
            return f"user with id {user_id} not found"

        foundUser.name = request.form["name"]
        foundUser.email = request.form["email"]

        db.session.commit()
        return f"User updated: {foundUser}"

    return f"The Update User Page"


@app.route("/deleteUser", methods=["GET", "DELETE"])
def deleteUser():
    if request.method == "DELETE":
        user_id = request.form["user_id"]
        if not user_id == session["user_id"] and not isAdmin:
            abort(404)

        foundUser = __getUser(user_id)
        if not foundUser:
            return f"User with id {user_id} not found"

        db.session.delete(foundUser)
        db.session.commit()

        if int(user_id) == session["user_id"]:
            session.pop("user_id", None)
            return redirect(url_for("login"))

        return f"User deleted: {foundUser}"

    return f"The Delete user Page"


# Run App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
