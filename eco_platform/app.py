import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Lesson, UserProgress, Badge, UserBadge
from werkzeug.security import generate_password_hash

app = Flask(__name__)
# Config
app.config['SECRET_KEY'] = 'menim_gizli_acar_sozum_123' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper to init DB
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create Hardcoded Admin
        admin_user = User.query.filter_by(username="Eyyub").first()
        if not admin_user:
            admin = User(
                username="Eyyub",
                lastname="Admin",
                role="admin",
                score=0,
                school="Platform",
                grade="AH",
                age=99,
                is_approved=True # Admin is always approved
            )
            admin.set_password("123456789")
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin 'Eyyub' created.")

        if not Lesson.query.first():
            # Lessons handled by populate.py mostly, but good to have empty check here if needed
            pass

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if not user.is_approved:
                flash('Hesabınız hələ Admin tərəfindən təsdiqlənməyib ⏳')
                return redirect(url_for('login'))
                
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('İstifadəçi adı və ya şifrə səhvdir!')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        lastname = request.form.get('lastname')
        school = request.form.get('school')
        grade = request.form.get('grade')
        age = request.form.get('age')
        
        if User.query.filter_by(username=username).first():
            flash('Bu ad artıq istifadə olunub.')
        else:
            new_user = User(
                username=username,
                lastname=lastname,
                school=school,
                grade=grade,
                age=age,
                role='student', # Always student
                is_approved=False # Wait for approval
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            # Do NOT login automatically
            flash('Qeydiyyat uğurludur! Admin təsdiqini gözləyin. ⏳')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/lessons')
@login_required
def lessons():
    all_lessons = Lesson.query.all()
    return render_template('lessons.html', lessons=all_lessons)

@app.route('/lesson/<int:lesson_id>')
@login_required
def lesson_detail(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('lesson_detail.html', lesson=lesson)

@app.route('/games')
@login_required
def games():
    return render_template('games.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/api/check_answer', methods=['POST'])
@login_required
def check_answer():
    data = request.json
    lesson_id = data.get('lesson_id')
    selected = data.get('option')
    
    lesson = Lesson.query.get_or_404(lesson_id)
    is_correct = (selected == lesson.correct_option)
    
    user = current_user
    
    if is_correct:
        progress = UserProgress.query.filter_by(user_id=user.id, lesson_id=lesson.id).first()
        if not progress:
            progress = UserProgress(user_id=user.id, lesson_id=lesson.id, score_earned=10)
            user.score += 10
            # user.stars is now dynamic property
            db.session.add(progress)
            db.session.commit()
            
    return jsonify({
        'correct': is_correct,
        'explanation': lesson.explanation,
        'new_score': user.score
    })

@app.route('/api/add_points', methods=['POST'])
@login_required
def add_points():
    data = request.json
    points = data.get('points', 0)
    if points > 0:
        current_user.score += points
        db.session.commit()
    return jsonify({'new_score': current_user.score})

@app.route('/game/sorting')
@login_required
def game_sorting():
    return render_template('game_sorting.html')

@app.route('/game/environment')
@login_required
def game_environment():
    return render_template('game_environment.html')

@app.route('/game/memory')
@login_required
def game_memory():
    return render_template('game_memory.html')

@app.route('/leaderboard')
def leaderboard():
    # Filter out admins, show only students
    users = User.query.filter(User.role != 'admin').order_by(User.score.desc()).limit(10).all()
    return render_template('leaderboard.html', users=users)

@app.route('/certificate')
@login_required
def certificate():
    if current_user.score >= 100:
        return render_template('certificate.html', user=current_user)
    else:
        return redirect(url_for('profile'))

# --- ADMIN PANEL ---
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return "Giriş qadağandır! Yalnız adminlər üçündür.", 403
    
    users = User.query.all()
    lessons = Lesson.query.all()
    total_users = len(users)
    total_lessons = len(lessons)
    
    return render_template('admin.html', users=users, lessons=lessons, stats={
        'total_users': total_users, 'total_lessons': total_lessons
    })

@app.route('/admin/approve/<int:user_id>')
@login_required
def approve_user(user_id):
    if current_user.role != 'admin':
        return "Access Denied", 403
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    if current_user.role != 'admin': return "Access Denied", 403
    user = User.query.get_or_404(user_id)
    if user.id != current_user.id: # Cannot delete self
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/init')
def initialize():
    init_db()
    # Ensure lessons exist if init_db empty skipped
    # (Simplified for this file write, assuming DB is fine from previous steps)
    return "DB Check"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
