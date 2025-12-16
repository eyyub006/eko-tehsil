from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Extended Profile
    lastname = db.Column(db.String(80))
    school = db.Column(db.String(120))
    grade = db.Column(db.String(10)) # e.g. "5A"
    age = db.Column(db.Integer)
    
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='student') # student, admin
    score = db.Column(db.Integer, default=0)
    is_approved = db.Column(db.Boolean, default=False) # New approval field
    
    @property
    def stars(self):
        # 1 Star for every 50 points
        return self.score // 50

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    # Relationships
    progress = db.relationship('UserProgress', backref='user', lazy=True)
    badges = db.relationship('UserBadge', backref='user', lazy=True)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    content = db.Column(db.Text, nullable=False)
    # Question data
    question_text = db.Column(db.String(500))
    option_a = db.Column(db.String(200)) # Simple 2 options for kids
    option_b = db.Column(db.String(200))
    correct_option = db.Column(db.String(1)) # 'A' or 'B'
    explanation = db.Column(db.Text) # Feedback after answer

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    score_earned = db.Column(db.Integer, default=0)

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(100), default='default_badge.png')
    description = db.Column(db.String(200))

class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
