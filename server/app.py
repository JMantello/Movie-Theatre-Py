from flask import Flask, redirect, url_for, request, abort, session, jsonify, make_response
from datetime import timedelta, datetime
from enum import Enum
import uuid
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
genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi']

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


def __getUserByEmail(user_email):
    return User.query.filter_by(email=user_email).first()


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user_id):
        self.user_id = user_id
        self.token = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


class SessionSchema(SQLAlchemySchema):
    class Meta:
        model = Session
        load_instance = True

    id = auto_field()
    user_id = auto_field()
    token = auto_field()
    created_at = auto_field()
    updated_at = auto_field()


def __getSessionByToken(token):
    return Session.query.filter_by(token=token).first()


def __getUserBySessionToken(token):
    session = __getSessionByToken(token)
    if not session:
        return None
    user = __getUser(session.user_id)
    return user


# Routes
@app.route('/dataSeed')
def dataSeed():
    fake = Faker()

    genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi']

    for i in range(50):
        content = Content(fake.sentence(), fake.text(),
                          fake.random_element(genres), fake.image_url())  # width=1920, height=1080

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

    return f"Database seeded", 200


@app.route("/login", methods=["POST"])
def login():
    req = request.get_json()

    email = req["email"]
    foundUser = __getUserByEmail(email)
    if not foundUser:
        return f"Invalid email or password", 400

    password = req["password"]
    if not foundUser.verify_password(password):
        return f"Invalid email or password", 400

    # Return token if existing session
    foundSession = Session.query.filter_by(user_id=foundUser.id).first()
    if foundSession:
        return jsonify(SessionSchema().dump(foundSession)), 200

    session = Session(foundUser.id)
    db.session.add(session)
    db.session.commit()

    return jsonify(SessionSchema().dump(session)), 200


@app.route("/logout", methods=["POST"])
def logout():
    req = request.get_json()

    foundSession = __getSessionByToken(req["token"])
    if (foundSession):
        db.session.delete(foundSession)
        db.session.commit()

    return f"Logged out", 200


@app.route("/feed", methods=["POST"])
def feed():
    req = request.get_json()
    print(req)
    user = __getUserBySessionToken(req["token"])
    if not user:
        return jsonify(f"No user found in Session table", 404)

    contentData = Content.query.all()

    cs = ContentSchema()
    feed = []
    for c in contentData:
        feed.append(cs.dump(c))

    return jsonify(feed)


@app.route("/watch", methods=["GET"])
def watch():
    req = request.get_json()
    user = __getUserBySessionToken(req["token"])
    if not user:
        return jsonify(f"No user found in Session table", 404)

    content = __getContent(req["content_id"])
    if not content:
        return 404

    if content not in user.watchHistory:
        user.watchHistory.append(content)
        db.session.commit()
        return 200


@app.route("/user", methods=["GET", "POST", "PUT", "DELETE"])
def user():
    if request.method == "POST":
        req = request.get_json()
        email = req["email"]
        foundUser = __getUserByEmail(email)
        if foundUser:
            return f"User already registered with that email", 400

        name = req["name"]
        password = req["password"]
        isAdmin = req["isAdmin"]

        user = User(name, email, password)
        if isAdmin:
            user.isAdmin = True
        db.session.add(user)

        user = __getUserByEmail(email)
        session = Session(user.id)
        db.session.add(session)
        db.session.commit()

        res = jsonify(SessionSchema().dump(session))
        return res

    if request.method == "GET":
        token = request.args["token"]
        user_id = request.args["user_id"]
        foundUser = __getUser(user_id)

        if not foundUser:
            return jsonify(f"No user found with id: {user_id}", 404)

        if not foundUser.isAdmin:
            abort(404)

        us = UserSchema()
        return jsonify(us.dump(foundUser))

    if request.method == "PUT":  # Updates
        req = request.get_json()
        token = req["token"]
        name = req["name"]
        email = req["email"]
        password = req["password"]
        isAdmin = req["isAdmin"]

        foundUser = __getUserBySessionToken(token)
        if not foundUser:
            return jsonify(f"No user found session: {token}", 404)

        if name:
            foundUser.name = req["name"]
        if email:
            foundUser.email = req["email"]
        if password:
            foundUser.password = password
        if isAdmin:
            foundUser.isAdmin = isAdmin

        db.session.commit()
        session = __getSessionByToken(token)
        res = jsonify(SessionSchema().dump(session))
        return res

    if request.method == "DELETE":
        token = request.args["token"]
        foundUser = __getUserBySessionToken(token)
        if not foundUser:
            return jsonify(f"No user found session: {token}", 404)
        if not foundUser.isAdmin:
            abort(404)

        # Delete user
        userToDelete = __getUser(request.args["user_id"])
        db.session.delete(userToDelete)

        # Delete Session as well
        session = __getSessionByToken(token)
        db.session.delete(session)

        db.session.commit()
        res = jsonify(UserSchema().dump(userToDelete))
        return res, 200


@app.route("/content", methods=["GET", "POST", "PUT", "DELETE"])
def content():
    if request.method == "GET":
        token = request.args["token"]

        foundUser = __getUserBySessionToken(token)
        if not foundUser:
            return jsonify(f"No user found session: {token}", 404)

        content = __getContent(request.args["content_id"])
        if not content:
            return f"Content not found", 404

        cs = ContentSchema()

        return jsonify(cs.dump(content))

    if request.method == "POST":
        req = request.get_json()

        user = __getUserBySessionToken(req["token"])
        if not user:
            return jsonify(f"No user found in Session table", 404)

        if not user.isAdmin:
            return abort(404)

        # require isAdmin to continue
        title = req["title"]
        description = req["description"]
        genre = req["genre"]
        image_url = req["image_url"]

        content = Content(title, description, genre, image_url)
        db.session.add(content)
        db.session.commit()

        # Need Fix: Return the newly added content
        return f"Content added", 200

    if request.method == "PUT":
        req = request.get_json()

        user = __getUserBySessionToken(req["token"])
        if not user:
            return jsonify(f"No user found in Session table", 404)

        foundContent = __getContent(req["content_id"])
        if not foundContent:
            return f"Content not found", 404

        title = req["title"]
        description = req["description"]
        genre = req["genre"]
        image_url = req["image_url"]

        # Update only fields included in request body
        if title:
            foundContent.title = title

        if description:
            foundContent.description = description

        if genre:
            foundContent.genre = genre

        if image_url:
            foundContent.image_url = image_url

        db.session.commit()

        # Need Fix: Return the newly updated content
        return f"Content updated", 200

    if request.method == "DELETE":
        token = request.args["token"]

        foundUser = __getUserBySessionToken(token)
        if not foundUser:
            return abort(404)  # Hides functionality

        if not foundUser.isAdmin:
            abort(404)

        foundContent = __getContent(request.args["content_id"])
        if not foundContent:
            return f"Content not found", 404

        db.session.delete(foundContent)
        db.session.commit()

        # Need Fix: Return the deleted content
        return f"Content deleted", 200


# Run App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
