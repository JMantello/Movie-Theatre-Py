from flask import Flask, redirect, url_for, request

app = Flask(__name__)
isAdmin = False


@app.route('/')
def index():
    return redirect(url_for("login"))


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return f"Username: {username}, Password: {password}"

    else:
        return "The Login Page"


@app.route('/param/<param>')
def param(param):
    return f"Param: {param}"


@app.route("/admin")
def admin():
    if not isAdmin:
        return redirect(url_for("login"))

    return redirect(url_for("param", param="Hello Admin"))


if __name__ == "__main__":
    app.run(debug=True)
