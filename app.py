from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import requests
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-super-secret-key-here-change-this-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///notes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

WAKATIME_API_BASE_URL = 'https://wakatime.com/api/v1'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    wakatime_api_key = db.Column(db.String(255), nullable=True)  
    notes = db.relationship('Note', backref='author', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_pinned = db.Column(db.Boolean, default=False)
    reminder_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attachments = db.relationship('Attachment', backref='note', lazy=True)

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    q = request.args.get('q', '').strip()
    query = Note.query.filter_by(user_id=current_user.id)
    if q:
        query = query.filter(
            (Note.title.ilike(f'%{q}%')) | (Note.content.ilike(f'%{q}%'))
        )
    notes = query.order_by(Note.is_pinned.desc(), Note.created_at.desc()).all()
    return render_template('dashboard.html', notes=notes, now=datetime.utcnow())


ALLOWED_EXTENSIONS=['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','doc', 'docx']


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_note', methods=['POST'])
@login_required
def add_note():
    title = request.form['title']
    content = request.form['content']
    reminder_date = request.form.get('reminder_date')

    if reminder_date and reminder_date.strip():
        try:
            reminder_date = datetime.strptime(reminder_date, '%Y-%m-%dT%H:%M')
        except ValueError:
            reminder_date = None
    else:
        reminder_date = None

    note = Note(
        title=title,
        content=content,
        reminder_date=reminder_date,
        user_id=current_user.id
    )
    db.session.add(note)
    db.session.commit()
    files = request.files.getlist('attachments')
    upload_folder = os.path.join(os.path.dirname(__file__), 'instance', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    for file in files:
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))
            attachment = Attachment(filename=filename, note_id=note.id)
            db.session.add(attachment)
    db.session.commit()

    flash('Note added successfully!')
    return redirect(url_for('dashboard'))


@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:
        flash('You can only edit your own notes!')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        note.reminder_date = None

        reminder_date = request.form.get('reminder_date')
        if reminder_date and reminder_date.strip():
            try:
                note.reminder_date = datetime.strptime(reminder_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                note.reminder_date = None

        db.session.commit()
        flash('Note updated successfully!')
        return redirect(url_for('dashboard'))

    return render_template('edit_note.html', note=note)

@app.route('/delete_note/<int:note_id>')
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:
        flash('You can only delete your own notes!')
        return redirect(url_for('dashboard'))

    upload_folder = os.path.join(os.path.dirname(__file__), 'instance', 'uploads')
    for attachment in note.attachments:
        try:
            file_path = os.path.join(upload_folder, attachment.filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass

    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully!')
    return redirect(url_for('dashboard'))

@app.route('/toggle_pin/<int:note_id>')
@login_required
def toggle_pin(note_id):
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    note.is_pinned = not note.is_pinned
    db.session.commit()

    return jsonify({'pinned': note.is_pinned})

@app.route('/reminders')
@login_required
def reminders():
    now = datetime.utcnow()
    upcoming_reminders = Note.query.filter(
        Note.user_id == current_user.id,
        Note.reminder_date.isnot(None),
        Note.reminder_date >= now
    ).order_by(Note.reminder_date).all()

    overdue_reminders = Note.query.filter(
        Note.user_id == current_user.id,
        Note.reminder_date.isnot(None),
        Note.reminder_date < now
    ).order_by(Note.reminder_date).all()

    return render_template('reminders.html',
                         upcoming_reminders=upcoming_reminders,
                         overdue_reminders=overdue_reminders)

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    upload_folder = os.path.join(os.path.dirname(__file__), 'instance', 'uploads')
    return send_from_directory(upload_folder, filename)

@app.route('/wakatime/settings', methods=['GET', 'POST'])
@login_required
def wakatime_settings():
    if request.method == 'POST':
        api_key = request.form.get('wakatime_api_key', '').strip()
        
        if api_key:
            headers = {'Authorization': f'Basic {api_key}'}
            try:
                response = requests.get(f'{WAKATIME_API_BASE_URL}/users/current', headers=headers)
                if response.status_code == 200:
                    current_user.wakatime_api_key = api_key
                    db.session.commit()
                    flash('WakaTime API key saved successfully!')
                else:
                    flash('Invalid WakaTime API key. Please check and try again.')
            except Exception as e:
                flash('Error validating API key. Please try again.')
        else:
            current_user.wakatime_api_key = None
            db.session.commit()
            flash('WakaTime API key cleared.')
        
        return redirect(url_for('wakatime_settings'))
    
    return render_template('wakatime_settings.html')

@app.route('/wakatime/stats')
@login_required
def wakatime_stats():
    if not current_user.wakatime_api_key:
        flash('Please set your WakaTime API key first.')
        return redirect(url_for('wakatime_settings'))
    
    headers = {'Authorization': f'Basic {current_user.wakatime_api_key}'}
    
    try:
        user_response = requests.get(f'{WAKATIME_API_BASE_URL}/users/current', headers=headers)
        if user_response.status_code != 200:
            flash('Error fetching WakaTime data. Please check your API key.')
            return redirect(url_for('wakatime_settings'))
        
        user_data = user_response.json()
        today = datetime.now().strftime('%Y-%m-%d')
        stats_response = requests.get(
            f'{WAKATIME_API_BASE_URL}/users/current/summaries',
            headers=headers,
            params={'start': today, 'end': today}
        )
        
        stats_data = {}
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
        
        return render_template('wakatime_stats.html', user_data=user_data, stats_data=stats_data)
        
    except Exception as e:
        flash('Error fetching WakaTime data. Please try again.')
        return redirect(url_for('wakatime_settings'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))