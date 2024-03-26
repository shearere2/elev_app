from flask import Flask, render_template, url_for
import re
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the web application."

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "index.html",
        name=name,
        date=datetime.now()
    )

if __name__ == "__main__":
    app.run()