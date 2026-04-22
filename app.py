import os
from cs50 import SQL
from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET KEY", os.urandom(24))


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")


@app.route("/")
@login_required
def index():
    messages = db.execute(
        """
        SELECT messages.id, message, timestamp, users.username, users.id as user_id
        FROM messages
        JOIN users ON messages.user_id = users.id
        ORDER BY timestamp ASC
    """
    )

    return render_template("index.html", messages=messages)


@app.route("/send", methods=["POST"])
@login_required
def send():
    messages = request.form.get("message")

    if messages:
        db.execute(
            "INSERT INTO messages (user_id, message) VALUES(?, ?)",
            session["user_id"],
            messages,
        )

    return redirect("/")


@app.route("/delete/<int:msg_id>", methods=["POST"])
@login_required
def delete(msg_id):

    msg = db.execute("SELECT * FROM messages WHERE id = ?", msg_id)

    if len(msg) != 1:
        flash("Message not found")
        return redirect("/")

    if msg[0]["user_id"] != session["user_id"]:
        flash("Not allowed")
        return redirect("/")

    db.execute("DELETE FROM messages WHERE id = ?", msg_id)

    flash("Message deleted")
    return redirect("/")


@app.route("/profile")
def profile():
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    if len(user) != 1:
        flash("User not found")
        return redirect("/")

    msg_count = db.execute(
        "SELECT COUNT(*) as count FROM messages WHERE user_id = ?", session["user_id"]
    )[0]["count"]

    return render_template("profile.html", user=user[0], msg_count=msg_count)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not email or not password or not confirmation:
            flash("Fill all the fields")
            return redirect("/register")

        if password != confirmation:
            flash("Password do not match")
            return redirect("/register")

        hash = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users(username, email, has, created_at) VALUES (?, ?, ?, DATETIME('NOW '))",
                username,
                email,
                hash,
            )
        except:
            flash("Username or email already exist")
            return redirect("/register")

        flash("Registered successfully!!")
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            flash("Enter email")
            return redirect("/login")

        if not password:
            flash("Enter password")
            return redirect("/login")

        rows = db.execute("SELECT * FROM users WHERE email = ?", email)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid credentials")
            return redirect("/login")

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    return render_template("login.html")


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form.get("email")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not email or not new_password or not confirm_password:
            flash("Fill all fields")
            return redirect("/forgot")

        if new_password != confirm_password:
            flash("Password do not match")
            return redirect("/forgot")

        rows = db.execute("SELECT * FROM users WHERE email = ?", email)

        if len(rows) != 1:
            flash("Email not found")
            return redirect("/forgot")

        hash = generate_password_hash(new_password)

        db.execute("UPDATE users SET hash = ? WHERE email = ?", hash, email)

        flash("Password updated successfully!")
        return redirect("/login")

    else:
        return render_template("forgot.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
