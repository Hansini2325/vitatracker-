from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import execute_query

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('logs.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('register.html')
        
        existing_user = execute_query(
            "SELECT user_id FROM users WHERE username = %s OR email = %s",
            (username, email),
            fetch_one=True
        )
        
        if existing_user:
            flash('Username or email already exists', 'error')
            return render_template('register.html')
        
        password_hash = generate_password_hash(password)
        
        result = execute_query(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password_hash)
        )
        
        if result:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('logs.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('login.html')
        
        user = execute_query(
            "SELECT user_id, username, password_hash FROM users WHERE username = %s",
            (username,),
            fetch_one=True
        )
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('logs.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = execute_query(
        "SELECT username, email, created_at FROM users WHERE user_id = %s",
        (session['user_id'],),
        fetch_one=True
    )
    
    vitamin_count = execute_query(
        "SELECT COUNT(*) as count FROM vitamins WHERE user_id = %s",
        (session['user_id'],),
        fetch_one=True
    )
    
    log_count = execute_query(
        "SELECT COUNT(*) as count FROM intake_logs WHERE user_id = %s",
        (session['user_id'],),
        fetch_one=True
    )
    
    return render_template('profile.html', 
                         user=user, 
                         vitamin_count=vitamin_count['count'] if vitamin_count else 0,
                         log_count=log_count['count'] if log_count else 0)