# app/routes/sec_auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.sec_model import User

# Blueprint name remains 'auth', as this is how you reference it in url_for.
# The file name is 'sec_auth.py', but the internal blueprint name is 'auth'.
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/")
def index():
    if 'user_id' not in session:
        return redirect(url_for("auth.login"))
    else:
        # Redirect to the task blueprint's view_task function
        return redirect(url_for("task.view_task"))

@auth_bp.route("/register")
def show_registration_form():
    # !!! IMPORTANT CHANGE HERE: Use your renamed template file 'sec_register.html' !!!
    return render_template("sec_register.html")

@auth_bp.route("/submit_registration", methods=["POST"])
def submit_registration():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password cannot be empty!", "error")
            return redirect(url_for("auth.show_registration_form"))

        existing_user = User.query.filter_by(username=username).first()# only first username from database is checked 

        if existing_user:
            flash(f"User '{username}' already exists. Please choose a different username.", "warning")
            return redirect(url_for("auth.show_registration_form"))

        new_user = User(username=username)
        new_user.set_password(password) # IN THIS WE DONT NEED TO CALL THE MAIN User MODEL VERY NICE 

        db.session.add(new_user)
        db.session.commit()

        flash(f"User '{username}' registered successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))
    return redirect(url_for("auth.show_registration_form"))

@auth_bp.route("/login" , methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Login Successful ", "success")
            # Redirect to the task blueprint's view_task function
            return redirect(url_for("task.view_task"))
        else:
            flash("Login failed. Check username and password.", "error")
    # !!! IMPORTANT CHANGE HERE: Use your renamed template file 'sec_login.html' !!!
    return render_template("sec_login.html")

@auth_bp.route("/logout",methods=["GET","POST"])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))