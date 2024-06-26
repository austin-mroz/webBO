from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# this file is a blueprint of our application

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form['action'] == 'submit':
            email = request.form.get("email")
            password = request.form.get("password")

            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash("logged in subbessfully!", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for("home_dash.home"))
                else:
                    flash("Incorrect password", category="error")
            else:
                flash("Username does not exist", category="error")
        elif request.form['action'] == 'signup':
            return redirect(url_for("auth.sign_up"))
        elif request.form['action'] == 'explore':
            pass

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Username already exists.", category="error")
        elif len(email) < 1:
            flash("Username is must be greater than 1 characters", category="error")
        elif len(first_name) < 2:
            flash("First name must possess more than 1 character", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        elif len(password1) < 7:
            flash("Password much be at least 7 characters", category="error")
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method="pbkdf2"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("home_dash.home"))

    return render_template("sign_up.html", user=current_user)