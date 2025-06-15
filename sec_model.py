# app/models.py
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# --- User Model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    tasks = db.relationship('Task', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def _repr_(self):
        return f"User('{self.username}', ID: {self.id}')"

# --- Task Model ---
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), default="Pending")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key: Linking Task to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def _repr_(self):
        return f"Task('{self.title}', Status: '{self.status}', User_ID: {self.user_id}')"