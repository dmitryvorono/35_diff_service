from flask_app.flask_server import app
from flask import render_template, request
import diff


@app.route("/")
def hello():
    return render_template('differ.html')


@app.route("/result", methods=['POST'])
def show_result_diff():
    initial_text = request.form['initial_text']
    emended_text = request.form['emended_text']
    diff_txt = diff.textDiff(initial_text, emended_text)
    return render_template('result.html', diff_txt=diff_txt)
