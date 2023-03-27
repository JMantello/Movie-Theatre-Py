from flask import Flask, redirect, url_for, request, abort, session
from datetime import timedelta
import sqlalchemy

app = Flask(__name__)
app.secret_key = "appsecretkey"
app.permanent_session_lifetime = timedelta(days=30)
isAdmin = False


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
    if "username" in session:
        sessionData = session["username"]
        return f"The Browse Page for {sessionData}"

    else:
        return redirect(url_for("login"))


@app.route("/youraccount", methods=["GET", "POST"])
def youraccount():
    if "username" in session:
        sessionData = session["username"]
        return f"The Browse Page for {sessionData}"

    else:
        return redirect(url_for("login"))


@app.route('/viewData/<data>')
def viewData(data):
    return f"Your Data: {data}"


@app.route("/admin")
def admin():
    if not isAdmin:
        abort(404)

    return redirect(url_for("param", param="Hello Admin"))


if __name__ == "__main__":
    app.run(debug=True)
