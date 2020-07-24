from flask import Flask,request,render_template,jsonify
from datetime import datetime
import todoist
import sqlite3
import requests

app = Flask(__name__)

db = 'data.db' #[Item ID, Time Estmate]
api = todoist.TodoistAPI('f84b92c505121b40a3489b4904b7eeb99ad11b7b')

@app.route('/')
def update_database():
    '''Retrieve new data and ensure the serverside database is up to date. Render the home template with updated data.'''
    api.sync() #Ensure the data is synced

    #access database and table
    conn = sqlite3.connect(db) 
    c = conn.cursor()  
    c.execute('''CREATE TABLE IF NOT EXISTS timetable (item_id int PRIMARY KEY, time_estimate real);''')

    #Ensure all the items are in the database (add new ones)
    for item in api.state['items']:
        c.execute('''INSERT OR IGNORE INTO timetable (item_id, time_estimate) \
            VALUES (?, 0);''', (item["id"],))
    
    #Close database connection
    conn.commit()
    conn.close()

    return render_template("home.html", data = api.state['items'], times = get_times())

@app.route('/get_times',methods=['GET', 'POST'])
def get_times():
    '''Return all the items and times in the database as a dictionary'''
    #connect to the database
    conn = sqlite3.connect(db) 
    c = conn.cursor()  

    #Get all items
    results = c.execute('''SELECT item_id, time_estimate FROM timetable;''').fetchall()

    #Add all items as a dictionary id:time
    obj = {}
    for x in results:
        obj[x[0]] = x[1]

    conn.commit() # commit commands
    conn.close() # close connection to database
    return obj

@app.route('/home')
def home():
    '''Update the database when home reloads'''
    update_database()
    return render_template("home.html", data = api.state['items'], times = get_times())

@app.route('/about')
def about():
    about_message = "Hello, I am Anna."
    return render_template("about.html", about_message = about_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return "GET"
    else:
        return "POST"

@app.route('/time', methods=['GET', 'POST'])
def time():
    conn = sqlite3.connect(db) 
    c = conn.cursor()  
    for arg in request.args:
        try:
            check = int(arg)
        except:
            return "Invalid input."
        c.execute('''UPDATE timetable SET time_estimate = ? WHERE item_id = ?''', (request.args[arg], arg))
        conn.commit()
    results = get_times()
    return render_template("home.html", data = api.state['items'], times = results)

if __name__ == '__main__':
    app.run(debug=True)