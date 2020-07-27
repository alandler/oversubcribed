#User sees the view

from flask import Flask, request, render_template, jsonify, abort, redirect, url_for, json
from datetime import datetime
import todoist
import sqlite3
import requests

from controller import Service

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    serv = Service()
    api = serv.sync()
    return render_template("home.html", data = api.state["items"], \
        times = serv.get_times(), days = serv.aggregate_by_day())

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/time', methods=['POST'])
def time():
    for item_id in request.form:
        try:
            check = float(request.form[item_id])
            serv = Service()
            serv.update_item(item_id, request.form[item_id])
        except:
            return "Invalid input."
    return redirect(url_for('home'))




if __name__ == '__main__':
    app.run(debug=True)