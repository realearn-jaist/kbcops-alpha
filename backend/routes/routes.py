from flask import render_template
from backend import app

@app.route("/")
def home():
    return render_template('index.html', title='Home', message='Hello Users, Welcome!!')
