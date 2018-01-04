from flask_app.flask_server import app
from flask import render_template


@app.route("/")
def hello():
    return render_template('differ.html')


@app.route("/result", methods=['POST'])
def show_result_diff():
    return render_template('result.html')
