from datetime import datetime
from flask import render_template
from HelloFlask import app

@app.route('/')
def home2025():
    return render_template(
        "2025home.html",
        title = "Team Friends 2025")

@app.route('/index')
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    return render_template(
        "index.html",
        title = "Team Friends Fantasy Football",
        message = "Hello, Flask!",
        content = " on " + formatted_now)

@app.route('/api/data')
def get_data():
    return app.send_static_file('data.json')


@app.route('/about')
def about():
    return render_template(
        "about.html",
        title = "About HelloFlask",
        content = "Example app page for Flask")