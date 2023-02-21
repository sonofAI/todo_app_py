from flask import Flask, render_template, request, session, redirect
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///todoapp.db")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return "67"
        elif not request.form.get("password") or request.form.get("password") != request.form.get("password_conf"):
            return "68"

        pwhash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), pwhash)

        return redirect("/login")
    
    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            return "69"
        
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return "70"

        session["user_id"] = rows[0]["id"]

        return redirect("/")
    
    else:
        return render_template("login.html")


@app.route("/")
def index():
    try:
        user = session["user_id"]
        usrinfo = db.execute("SELECT * FROM todos WHERE user_id = ?", user)
        return render_template("layout.html", usrinfo=usrinfo)

    except KeyError:
        return redirect("/login")


@app.route("/todos", methods=["POST", "GET", "DELETE"])
def todos():
    if request.method == "POST":
        title = request.json["doc_title"]
        todo_item = request.json["todo_title"]
        db.execute("INSERT INTO todos (title, todo_item, user_id) VALUES (?, ?, ?)", title, todo_item, session["user_id"])

    elif request.method == "GET":
        todo_items = db.execute("SELECT * FROM todos WHERE user_id = ?", session["user_id"])
        return todo_items

    elif request.method == "DELETE":
        item_to_remove = request.json
        db.execute("DELETE FROM todos WHERE todo_item LIKE ? AND user_id = ?", item_to_remove, session["user_id"])

    return "69"


@app.route("/check", methods=["POST", "GET"])
def check():
    if request.method == "POST":
        status = request.json["status"]
        checked_item = request.json["checked_item"]
        db.execute("UPDATE todos SET status = ? WHERE todo_item LIKE ?", status, checked_item)
        return "done"

    return "You are not supposed to see this..."