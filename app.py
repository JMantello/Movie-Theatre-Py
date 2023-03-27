from flask import Flask, redirect, url_for, request, abort, session
from datetime import timedelta
import sqlalchemy

app = Flask(__name__)
app.secret_key = "appsecretkey"
app.permanent_session_lifetime = timedelta(days=30)
isAdmin = True


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

    else:
        return "The Login Page"


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/browse")
def browse():
    loginIfNoSession()

    sessionData = session["username"]
    return f"The Browse Page for {sessionData}"


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


@app.route("/addShow", methods=["GET", "POST"])
def addShow():
    if not isAdmin:
        abort(404)

    loginIfNoSession()

    if request.method == "POST":
        title = request.form["title"]
        return f"Show added: {title}"

    else:
        return f"The Add Show Page"


# Helper Functions
def loginIfNoSession():
    if "username" not in session:
        return redirect(url_for("login"))


# Run App
if __name__ == "__main__":
    app.run(debug=True)
