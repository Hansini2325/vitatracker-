from flask import Flask, render_template, session, redirect, url_for
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from routes import auth, vitamins, schedule, logs

app.register_blueprint(auth.bp)
app.register_blueprint(vitamins.bp)
app.register_blueprint(schedule.bp)
app.register_blueprint(logs.bp)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('logs.dashboard'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
