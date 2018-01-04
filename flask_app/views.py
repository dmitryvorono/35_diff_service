from flask_app.flask_server import app


@app.route("/")
def hello():
    return "Hello Differ!"