
from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint, session# error in session but why i dont know 
# usijng auth which is name inside blueprint it is connected to all the routes 
auth_bp=Blueprint('auth',__name__)
user_credential={}
@auth_bp.route("/" , methods=["GET"])#typo
def default():
    return render_template("register.html")
@auth_bp.route("/register", methods=["post","GET"])
def register():
    if request.method == "POST":
        username=request.form.get("R_username")
        password=request.form.get('R_password')
        if not username or not password:
            flash("plz enter your username and password")
        if username in user_credential:
            flash("Username already exist Try another. Warning!")
            return redirect(url_for("auth.default"))
        user_credential[username]=password
        flash("{username} Registered Successfully !")
    return render_template("login.html")


@auth_bp.route("/login" , methods=["POST","GET"])#typo
def login():
    if request.method == "POST":
        username=request.form.get('username')
        password=request.form.get('password')
        if username in user_credential and str(user_credential[username]) == password:# error in logic 
            
            session['user']=username
            flash("Login Successful ")
            return redirect(url_for("task.view_task"))
        else:
            flash("login failed")
    return render_template("login.html")

@auth_bp.route("/logout",methods=["GET","POST"])#typo 
def logout():
    session.pop('user',None)
    flash("Logout Successfully")
    return redirect(url_for("auth.login"))

