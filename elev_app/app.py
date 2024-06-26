from flask import Flask, render_template, url_for, request
import re
from datetime import datetime

from elev_tools import summarize_journey

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

@app.route("/journey/")
@app.route("/journey/<coords>")
def journey(coords:str=None):
    if coords is None:
        return render_template("input.html")
    coords = coords.split('_')
    start = (coords[0],coords[1])
    end = (coords[2],coords[3])
    info = summarize_journey(start,end)
    return render_template(
        "input.html",
        up = '{0:.2f}'.format(info['Cumulative Uphill Travel']),
        down = '{0:.2f}'.format(info['Cumulative Downhill Travel']),
        alt = '{0:.2f}'.format(info['Total Altitude Change']),
        dist = '{0:.2f}'.format(info['Total Distance']),
        coords = coords
    )

@app.route('/input')
def my_form():
    return render_template('my-form.html')

@app.route('/input', methods=['POST'])
def my_form_post():
    slat = request.form['start_lat']
    slon = request.form['start_lon']
    elat = request.form['end_lat']
    elon = request.form['end_lon']
    start = tuple((slat,slon))
    end = tuple((elat,elon))
    coords = [start,end]
    info = summarize_journey(start,end)
    up = info['Cumulative Uphill Travel']
    down = info['Cumulative Downhill Travel']
    alt = info['Total Altitude Change']
    dist = info['Total Distance']
    return render_template(
        "input.html",
        up = '{0:.2f}'.format(info['Cumulative Uphill Travel']),
        down = '{0:.2f}'.format(info['Cumulative Downhill Travel']),
        alt = '{0:.2f}'.format(info['Total Altitude Change']),
        dist = '{0:.2f}'.format(info['Total Distance']),
        coords = coords
    )

if __name__ == "__main__":
    app.run()