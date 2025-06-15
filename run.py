# # from app import create_app,db
# # from app.model import Task

# # app= create_app()

# # with app.app_context():
# #     db.create_all()
# # if __name__== '__main__':
# #     app.run(debug=True)

# from app import create_app,db
# from app.model import Task

# # Create the app instance
# app = create_app()

# if __name__ == '__main__':
#     # Ensure database creation happens within the app context and only when run directly
#     with app.app_context():
#         db.create_all() # This will create tables if they don't exist

#     # Run the Flask development server
#     app.run(debug=True)
# run.py
# run.py
from app import create_app, db # Import the create_app function and the db instance from your 'app' package
from app.sec_model import User, Task # Import your User and Task models. This is useful for 'flask shell' context.

# Call the create_app function to get your configured Flask application instance.
app = create_app()

# --- Flask Shell Context (Optional but Recommended for Development) ---
# This decorator makes 'db', 'User', and 'Task' objects available in the 'flask shell' command.
# You can run 'flask shell' in your terminal (after activating venv and setting FLASK_APP)
# to interact with your database models directly (e.g., User.query.all()).
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task}

# --- Application Run Command ---
if __name__ == '__main__':
    # This block ensures the application only runs when the script is executed directly (not when imported as a module).
    # debug=True:
    #   1. Enables Flask's interactive debugger in the browser for errors (very helpful during development).
    #   2. Automatically reloads the server when you make code changes, so you don't have to restart it manually.
    # !!! IMPORTANT: You MUST set debug=False in a production environment for security and performance reasons.
    app.run(debug=True)