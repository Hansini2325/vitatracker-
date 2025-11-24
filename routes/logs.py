from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.db import execute_query
from datetime import datetime

bp = Blueprint('logs', __name__)

@bp.route('/dashboard')
def dashboard():
    uid = session.get('user_id')
    if not uid:
        return redirect(url_for('auth.login'))

    # get user's defined vitamins
    vits = execute_query(
        "SELECT * FROM vitamins WHERE user_id = %s ORDER BY name", 
        (uid,)
    )
    
    # get logs for today only
    # quick date string for query
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    # straightforward join to get names
    sql = """
        SELECT l.log_id, l.taken_at, v.name, v.dosage 
        FROM intake_logs l
        JOIN vitamins v ON l.vitamin_id = v.vitamin_id
        WHERE l.user_id = %s AND DATE(l.taken_at) = %s
        ORDER BY l.taken_at DESC
    """
    
    daily_logs = execute_query(sql, (uid, today_str))

    return render_template('dashboard.html', 
        vitamins=vits, 
        logs=daily_logs,
        today=datetime.now()
    )

@bp.route('/add-vitamin', methods=['POST'])
def add_vitamin():
    uid = session.get('user_id')
    if not uid: return redirect(url_for('auth.login'))

    # accessing form directly
    name = request.form.get('name', '').strip()
    dosage = request.form.get('dosage', '').strip()

    if not name:
        flash('Vitamin name is required.', 'error')
    else:
        # standard insert
        execute_query(
            "INSERT INTO vitamins (user_id, name, dosage) VALUES (%s, %s, %s)",
            (uid, name, dosage)
        )
        flash('Added successfully.', 'success')

    return redirect(url_for('logs.dashboard'))

# Note: Using GET here so we can just use a simple link in the HTML
# e.g. <a href="...">Take</a> instead of a form
@bp.route('/track/<int:vid>')
def track_intake(vid):
    uid = session.get('user_id')
    if not uid: return redirect(url_for('auth.login'))

    # verify vitamin belongs to user first
    check = execute_query(
        "SELECT vitamin_id FROM vitamins WHERE vitamin_id = %s AND user_id = %s",
        (vid, uid), fetch_one=True
    )

    if check:
        execute_query(
            "INSERT INTO intake_logs (user_id, vitamin_id, taken_at) VALUES (%s, %s, NOW())",
            (uid, vid)
        )
        flash('Logged.', 'success')
    else:
        flash('Error: Item not found.', 'error')

    return redirect(url_for('logs.dashboard'))

@bp.route('/delete-log/<int:lid>')
def delete_log(lid):
    uid = session.get('user_id')
    
    # basic ownership check + delete in one go ideally, 
    # but separate check is fine too
    execute_query(
        "DELETE FROM intake_logs WHERE log_id = %s AND user_id = %s",
        (lid, uid)
    )
    
    flash('Entry removed.', 'info')
    return redirect(url_for('logs.dashboard'))

@bp.route('/delete-vitamin/<int:vid>')
def delete_vitamin(vid):
    uid = session.get('user_id')

    # this might fail if foreign keys exist in logs, 
    # but letting sql throw the error is a very human thing to do
    try:
        execute_query(
            "DELETE FROM vitamins WHERE vitamin_id = %s AND user_id = %s",
            (vid, uid)
        )
        flash('Vitamin deleted.', 'success')
    except:
        flash('Cannot delete this item (it might have logs attached).', 'error')

    return redirect(url_for('logs.dashboard'))
