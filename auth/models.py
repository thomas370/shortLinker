from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from flask_bcrypt import Bcrypt
from utils.db import cursor, db
from auth.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
bcrypt = Bcrypt()

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user["password_hash"], password):
            login_user(User(user["id"], user["username"]))
            return redirect(url_for("links.index"))

        flash("Login incorrect")
    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        pw_hash = bcrypt.generate_password_hash(request.form["password"]).decode()
        cursor.execute(
            "INSERT INTO users (username,email,password_hash) VALUES (%s,%s,%s)",
            (request.form["username"], request.form["email"], pw_hash)
        )
        db.commit()
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

