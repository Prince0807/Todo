# app/routes/sec_task.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.sec_model import Task, User
from functools import wraps

# Blueprint name remains 'task', as this is how you reference it in url_for.
# The file name is 'sec_task.py', but the internal blueprint name is 'task'.
task_bp = Blueprint('task', "__name__")

# --- Custom Decorator: Ensures User is Logged In for Protected Routes ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login')) # Redirect to the 'auth' blueprint's login function
        return f(*args, **kwargs)
    return decorated_function

# --- View and Add Tasks Route (User-Specific) ---
@task_bp.route("/tasks", methods=["GET", "POST"])
@login_required
def view_task():
    user_id = session.get('user_id')
    username = session.get('username', 'Guest')

    if request.method == "POST":
        task_title = request.form.get('title')
        if not task_title:
            flash("Task title cannot be empty!", "error")
            return redirect(url_for("task.view_task"))

        new_task = Task(title=task_title, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", "success")
        return redirect(url_for("task.view_task"))

    user_tasks = Task.query.filter_by(user_id=user_id).order_by(Task.date_created.desc()).all()

    # !!! IMPORTANT CHANGE HERE: Use your renamed template file 'sec_task.html' !!!
    return render_template("sec_task.html", user_tasks=user_tasks,username=username)

# --- Delete Task Route (Ensures User Can Only Delete Their Own Tasks) ---
@task_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    user_id = session.get('user_id')

    task_to_delete = Task.query.filter_by(id=id, user_id=user_id).first()

    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash("Task deleted successfully!", "info")
    else:
        flash("Task not found or you don't have permission to delete it.", "error")
    return redirect(url_for('task.view_task'))