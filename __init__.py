# # from flask import Flask
# # from flask_sqlalchemy import SQLAlchemy

# # db=SQLAlchemy()

# # def create_app():
# #     app=Flask(__name__)
# #     app.config['SECRET_KEY']= "MY1234"
# #     app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql//root:PRINCE9800@#@#@localhost/make"
# #     app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
# #     db.__init__(app)
    
# #     #importing blueprint of task and auth.py
# #     from app.routes.auth import auth_bp
# #     from app.routes.task import task_bp# may be error 
# # # we are registaring because it should act as a module or samll application 
# #     app.register_blueprint(auth_bp)
# #     app.register_blueprint(task_bp)
# #     return app
# # app/__init__.py
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import urllib.parse # Import urllib.parse to encode the password

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = "MY1234"

#     # Correct and URL-encode your password
#     # Original: PRINCE9800@#@#@
#     # Encoded: PRINCE9800%40%23%40%23%40
#     # Note: I'm assuming 'PRINCE9800@#@#@' is the literal password.
#     # If the password is 'PRINCE9800' and you meant to add '@#@#@localhost',
#     # then you have extra characters there.
#     # Assuming 'PRINCE9800@#@#@' is the password for 'root'.
#     encoded_password = urllib.parse.quote_plus("PRINCE9800@#@#@")

#     # Corrected database URI
#     # Use 'mysql+pymysql://user:password@host/database_name' format
#     app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:{encoded_password}@localhost/make"

#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.init_app(app) # Use init_app instead of __init__ directly after instantiating

#     # Importing blueprints
#     from app.routes.auth import auth_bp
#     from app.routes.task import task_bp

#     app.register_blueprint(auth_bp)
#     app.register_blueprint(task_bp)
#     return app

# if __name__ == '__main__':
#     app = create_app() # You need to call create_app here
#     with app.app_context():
#         db.create_all() # db.create_all() not db.createall() (typo)
#     app.run(debug=True)
# app/_init_.py
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # --- Application Configuration ---
    app.config['SECRET_KEY'] = 'your_super_secret_key_that_you_must_change_for_security_12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    # --- Initialize Extensions ---
    db.init_app(app)

    

    # --- Register Blueprints ---
    # !!! IMPORTANT CHANGE HERE: Update import paths to match your 'sec_auth.py' and 'sec_task.py' file names !!!
    from .routes.sec_auth import auth_bp # Import 'auth_bp' from 'sec_auth.py'
    from .routes.sec_task import task_bp # Import 'task_bp' from 'sec_task.py'
    app.register_blueprint(auth_bp) # Register the authentication blueprint (blueprint name is still 'auth')
    app.register_blueprint(task_bp) # Register the task management blueprint (blueprint name is still 'task')

    # --- Database Table Creation (For Development Only) ---
    with app.app_context():
        db.create_all()

    return app