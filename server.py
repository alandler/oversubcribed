from flask import Flask
from flask import request
from datetime import datetime
import todoist
import sqlite3
import requests

app = Flask(__name__)

db = 'data.db' #[Item ID, Project ID, Content, Due Date, Priority, Time Estmate]
api = todoist.TodoistAPI('f84b92c505121b40a3489b4904b7eeb99ad11b7b')
api.sync()

def update_database():
    #access database and table
    conn = sqlite3.connect(db) 
    c = conn.cursor()  
    c.execute('''CREATE TABLE IF NOT EXISTS timetable (item_id real PRIMARY KEY, project_id real, content text, due_date timestamp, priority real, time_estimate real);''')

    for item in api.state['items']:
        try:
            four = datetime.strptime(item["due"]["date"], "%Y-%m-%s")
        except:
            four = datetime(year = 2050, month = 1, day = 1, hour = 0, minute = 0, second = 0)
        one = item["id"]
        two = item["project_id"]
        three = item["content"]
        five = item["priority"]

        c.execute('''INSERT OR REPLACE INTO timetable (item_id, project_id, content, due_date, priority, time_estimate) \
            VALUES (?, ?, ?, ?, ?, 0);''', (one,two,three,four,five))
    conn.commit()
    conn.close()

#update_database()

@app.route('/all')
def all():
    conn = sqlite3.connect(db) 
    c = conn.cursor()  
    results = c.execute('''SELECT item_id, time_estimate FROM timetable;''').fetchall()
    out = "Items"
    for x in results:
        out+=str(x)+"\n"
    conn.commit() # commit commands
    conn.close() # close connection to database
    return out
    

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return "GET"
    else:
        return "POST"