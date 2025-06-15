
# from flask import Blueprint, render_template, redirect, url_for, session, flash, request
# from app.model import Task
# from app import db
# task_bp=Blueprint('task',"__name__")
# @task_bp.route("/",methods=["GET","POST"])
# def log():
#     if 'user' not in session:
#         return redirect(url_for("auth.login"))
#     tasks = Task.query.all()
#     return render_template("login.html",task=tasks)
# @task_bp.route("/view_task",methods=["POST","GET"])
# def view_task():
#     if 'user' not in session:
#         return redirect(url_for("auth.login"))
#     tasks= Task.query.all()
#     return render_template("task.html",task=tasks)
# @task_bp.route("/add_task",methods=["POST"])
# def add_task():
#     if 'user' not in session:# error in ""
#         return redirect(url_for("auth.login"))
    
#     title=request.form.get("title")
#     if title:
#         new_task=Task(title=title,status="pending")
#         db.session.add(new_task)
#         db.session.commit()
#         flash("New Task added successfully !")
#     return redirect(url_for("task.view_task"))
# @task_bp.route("/toggle/<int:id>",methods=["POST"])
# def toggle(id):
#     task_id=Task.query.get(id)# we use variable for things which are not constant means which will keep changing and doubt is why we use Task not db ?
#     if task_id:
#         if task_id.status=="pending":
#             task_id.status="working"
#         elif task_id.status=="working":
#             task_id.status="done"
#         else:
#             task_id.status="pending"
#         db.session.commit()
#     return redirect(url_for("task.view_task"))
# @task_bp.route("/delete/<int:id>",methods=["POST"])
# def delete(id):
#     task_delete=Task.query.get(id)
#     db.session.delete(task_delete)# error can occur and it occured
#     db.session.commit()
#     flash(f"{task_delete}  task deleted ")#error f
#     return redirect(url_for("task.view_task"))
# @task_bp.route("/all_delete",methods=["POST"])
# def all_delete():
   
#     Task.query.delete()
#     db.session.commit()
#     flash(" All  task deleted ")
#     return redirect(url_for("task.view_task"))

from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from app.model import Task
from app import db # Assuming 'db' is initialized in app/__init__.py

task_bp = Blueprint('task', __name__)

@task_bp.route("/view_task", methods=["POST", "GET"])
def view_task():
    if 'user' not in session:
        flash("Please log in to view tasks.", "warning") # Added flash message category
        return redirect(url_for("auth.login"))
    
    tasks = Task.query.all() # Renamed 'task' to 'tasks' for clarity (list of Task objects)
    return render_template("task.html", task=tasks) # Pass the list of tasks to the template

@task_bp.route("/add_task", methods=["POST"])
def add_task():
    if 'user' not in session: # This check is correct
        flash("Please log in to add tasks.", "warning") # Added flash message category
        return redirect(url_for("auth.login"))
    
    title = request.form.get("title")
    if title:
        new_task = Task(title=title, status="Pending")
        db.session.add(new_task)
        db.session.commit()
        flash("New Task added successfully!", "success") # Added flash message category
    else:
        flash("Task title cannot be empty!", "error") # Added error flash message
    return redirect(url_for("task.view_task"))

@task_bp.route("/toggle/<int:id>", methods=["POST"]) # Added POST method
def toggle(id):
    # Answer to your doubt: We use `Task.query.get(id)` because `Task` is your SQLAlchemy model
    # that represents the table. `Task.query` allows you to build queries against that table.
    # `db` is the SQLAlchemy extension instance itself, used for session management (`db.session`)
    # and creating tables (`db.create_all()`).
    task_to_toggle = Task.query.get(id) 
    
    if 'user' not in session: # Added session check here too
        flash("Please log in to toggle task status.", "warning")
        return redirect(url_for("auth.login"))

    if task_to_toggle: # Check if task exists before attempting to modify
        if task_to_toggle.status == "Pending":
            task_to_toggle.status = "Working"
        elif task_to_toggle.status == "Working":
            task_to_toggle.status = "Completed"
        else: # If status is "Completed" or anything else, cycle back to "Pending"
            task_to_toggle.status = "Pending"
        db.session.commit()
        flash(f"Task '{task_to_toggle.title}' status updated to {task_to_toggle.status}!", "info")
    else:
        flash("Task not found for toggling!", "error") # Inform user if task doesn't exist
    return redirect(url_for("task.view_task"))

@task_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if 'user' not in session: # Added session check here too
        flash("Please log in to delete tasks.", "warning")
        return redirect(url_for("auth.login"))
        
    task_to_delete = Task.query.get(id) # Renamed for clarity
    
    # IMPORTANT FIX: Check if task_to_delete exists before attempting to delete it
    if task_to_delete: 
        db.session.delete(task_to_delete) # Correct way to delete a specific instance
        db.session.commit()
        # IMPORTANT FIX: Use .title to get the actual task title for the flash message
        flash(f"Task '{task_to_delete.title}' deleted successfully!", "success") # Added flash message category
    else:
        flash("Task not found for deletion!", "error") # Inform user if task doesn't exist

    return redirect(url_for("task.view_task"))

@task_bp.route("/all_delete", methods=["POST"])
def all_delete():
    if 'user' not in session: # Added session check here too
        flash("Please log in to delete all tasks.", "warning")
        return redirect(url_for("auth.login"))
        
    # More explicit way to delete all records from the Task table
    num_deleted = db.session.query(Task).delete() 
    db.session.commit()
    flash(f"{num_deleted} tasks deleted successfully!", "success") # Added flash message category
    return redirect(url_for("task.view_task"))
