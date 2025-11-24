from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.db import execute_query

bp = Blueprint('schedule', __name__, url_prefix='/schedule')

@bp.route('/')
def list_schedules():
    uid = session.get('user_id')
    if not uid:
        return redirect(url_for('auth.login'))

    # fetch all schedules with vitamin info
    # keeping the query simple
    sql = """
        SELECT s.schedule_id, s.time_of_day, s.days_of_week, v.name, v.dose
        FROM schedules s
        JOIN vitamins v ON s.vitamin_id = v.vitamin_id
        WHERE s.user_id = %s
        ORDER BY s.time_of_day ASC
    """
    
    rows = execute_query(sql, (uid,))
    
    return render_template('schedule.html', schedules=rows or [])

@bp.route('/add', methods=['GET', 'POST'])
def add_schedule():
    uid = session.get('user_id')
    if not uid: return redirect(url_for('auth.login'))

    # Always need the list for the dropdown
    v_list = execute_query(
        "SELECT vitamin_id, name FROM vitamins WHERE user_id = %s ORDER BY name",
        (uid,)
    )

    if request.method == 'POST':
        f = request.form
        vid = f.get('vitamin_id')
        t_time = f.get('time_of_day', '').strip()
        days = request.form.getlist('days_of_week') # getlist is needed for checkboxes

        if not vid or not t_time:
            flash('Missing required fields.', 'error')
            return render_template('add_schedule.html', vitamins=v_list)

        # default to Daily if nothing checked
        d_str = ','.join(days) if days else 'Daily'

        try:
            execute_query(
                "INSERT INTO schedules (user_id, vitamin_id, time_of_day, days_of_week) VALUES (%s, %s, %s, %s)",
                (uid, vid, t_time, d_str)
            )
            flash('Schedule saved.', 'success')
            return redirect(url_for('schedule.list_schedules'))
            
        except Exception as e:
            flash('Error saving schedule.', 'error')
            print(f"Schedule Add Error: {e}")

    return render_template('add_schedule.html', vitamins=v_list or [])

# Changed to GET so we can just use a link in the html
# e.g. <a href="/schedule/delete/5">Delete</a>
@bp.route('/delete/<int:sid>')
def delete_schedule(sid):
    uid = session.get('user_id')
    if not uid: return redirect(url_for('auth.login'))

    execute_query(
        "DELETE FROM schedules WHERE schedule_id = %s AND user_id = %s",
        (sid, uid)
    )
    
    flash('Removed.', 'success')
    return redirect(url_for('schedule.list_schedules'))
