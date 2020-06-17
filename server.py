from flask import Flask,request,render_template  
from datetime import datetime
import todoist
import sqlite3
import requests

app = Flask(__name__)

db = 'data.db' #[Item ID, Project ID, Content, Due Date, Priority, Time Estmate]
api = todoist.TodoistAPI('f84b92c505121b40a3489b4904b7eeb99ad11b7b')
api.sync()

about_message = "BUTT"

def update_database():
    #access database and table
    conn = sqlite3.connect(db) 
    c = conn.cursor()  
    c.execute('''CREATE TABLE IF NOT EXISTS timetable (item_id real PRIMARY KEY, time_estimate real);''')

    for item in api.state['items']:
        one = item["id"]
        c.execute('''INSERT OR REPLACE INTO timetable (item_id, time_estimate) \
            VALUES (?, ?, ?, ?, ?, 0);''', (one,))
    conn.commit()
    conn.close()

update_database()

@app.route('/')
def home():
    data = retrieve_from_database()

def retrieve_from_database():
    conn = sqlite3.connect(db) 
    c = conn.cursor()  
    results = c.execute('''SELECT item_id, time_estimate FROM timetable;''').fetchall()
    out = "Items"
    for x in results:
        out+=str(x)+"\n"
    conn.commit() # commit commands
    conn.close() # close connection to database
    return out
    
@app.route('/about')
def about():
    return render_template("about.html", about_message = about_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return "GET"
    else:
        return "POST"