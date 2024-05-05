from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user

from models.user import User

login_manager = LoginManager()
auth = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    """provide the user to the authentication system"""
    return User.getone(user_id)


@auth.get("/login")
def login_page():
    """GET the login page"""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    return render_template("login-page.html")


@auth.get("/logout")
def logout():
    """log out the user"""
    logout_user()
    return redirect("/login")


@auth.post("/login")
def login():
    """Submit the login form"""
    username = request.form.get("username")
    password = request.form.get("password")
    remember = request.form.get("remember") == "on"
    if not (username and password):
        error = "Please fill all the fields"
        return render_template("login-page.html", error=error)
    user = User.by_username(username)
    if not (user and user.check_password(password)):
        error = "Wrong username or password"
        return render_template(
            "login-page.html",
            username=username,
            password=password,
            remember=remember,
            error=error,
        )
    login_user(user, remember=remember)
    next_page = request.args.get("next", "/")
    return redirect(next_page)


@auth.get("/register")
def register_page():
    """GET the register page"""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    return render_template("register-page.html")


@auth.post("/register")
def register():
    """Submit the registration form"""
    print(request.form)
    return render_template("register-page.html")
