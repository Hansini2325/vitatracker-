from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.db import execute_query

bp = Blueprint('vitamins', __name__, url_prefix='/vitamins')

@bp.route('/')
def list_vitamins():
    uid = session.get('user_id')
    if not uid:
        return redirect(url_for('auth.login'))

    # simple select, descending order
    v_list = execute_query(
        "SELECT * FROM vitamins WHERE user_id = %s ORDER BY created_at DESC",
        (uid,)
    )
    
    # passing 'vitamins' to template to keep html happy
    return render_template('vitamins.html', vitamins=v_list or [])

@bp.route('/add', methods=['GET', 'POST'])
def add_vitamin():
    uid = session.get('user_id')
    if not uid: return redirect(url_for('auth.login'))

    if request.method == 'POST':
        f = request.form
        n = f.get('name', '').strip()
        d = f.get('dose', '').strip()
        freq = f.get('frequency', '')
        notes = f.get('notes', '')

        if not n:
            flash('Name is required.', 'error')
            return render_template('add_vitamin.html')

        execute_query(
            "INSERT INTO vitamins (user_id, name, dose, frequency, notes) VALUES (%s, %s, %s, %s, %s)",
            (uid, n, d, freq, notes)
        )
        
        flash('Saved.', 'success')
        return redirect(url_for('vitamins.list_vitamins'))

    return render_template('add_vitamin.html')

@bp.route('/edit/<int:vid>', methods=['GET', 'POST'])
def edit_vitamin(vid):
    uid = session.get('user_id')
    if not uid: return redirect(url_for('auth.login'))

    # fetch existing
    v = execute_query(
        "SELECT * FROM vitamins WHERE vitamin_id = %s AND user_id = %s",
        (vid, uid), fetch_one=True
    )

    if not v:
        flash('Vitamin not found.', 'error')
        return redirect(url_for('vitamins.list_vitamins'))

    if request.method == 'POST':
        f = request.form
        n = f.get('name', '').strip()
        
        # simple validation
        if not n:
            flash('Name cannot be empty', 'error')
            return render_template('edit_vitamin.html', vitamin=v)

        # Update params
        params = (
            n, 
            f.get('dose', ''), 
            f.get('frequency', ''), 
            f.get('notes', ''), 
            vid, 
            uid
        )
        
        execute_query(
            "UPDATE vitamins SET name=%s, dose=%s, frequency=%s, notes=%s WHERE vitamin_id=%s AND user_id=%s",
            params
        )
        
        flash('Changes saved.', 'success')
        return redirect(url_for('vitamins.list_vitamins'))

    return render_template('edit_vitamin.html', vitamin=v)

# changed to GET for easy link access
@bp.route('/delete/<int:vid>')
def delete_vitamin(vid):
    uid = session.get('user_id')
    if not uid: return redirect(url_for('auth.login'))

    execute_query(
        "DELETE FROM vitamins WHERE vitamin_id = %s AND user_id = %s",
        (vid, uid)
    )
    
    flash('Deleted.', 'info')
    return redirect(url_for('vitamins.list_vitamins'))
