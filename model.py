from datetime import datetime
import todoist
import sqlite3
import requests

api = todoist.TodoistAPI('f84b92c505121b40a3489b4904b7eeb99ad11b7b')

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_times_table()
    
    def create_times_table(self):
        query = """ CREATE TABLE IF NOT EXISTS Times (item_id INTEGER PRIMARY KEY, estimate real); """
        self.conn.execute(query)


class Todo:
    def __init__(self):
        Schema()
        self.conn = sqlite3.connect('todo.db')

    def sync(self):
        '''Sync the API and database; new items assigned a time estimate of 0'''
        api.sync()

        #access database and table
        c = self.conn.cursor()  
        c.execute('''CREATE TABLE IF NOT EXISTS Times (item_id int PRIMARY KEY, estimate real);''')

        #Ensure all the items are in the database (add new ones)
        for item in api.state['items']:
            c.execute('''INSERT OR IGNORE INTO Times (item_id, estimate) \
                VALUES (?, 0);''', (item["id"],))
        
        #Commit to database
        self.conn.commit()

        print("Finished sync")

        return api

    def update_item(self, item_id, estimate):
        '''Given an item and time estimate, input into the database'''
        c = self.conn.cursor()  
        c.execute('''UPDATE Times SET estimate = ? WHERE item_id = ?;''', (estimate,item_id))
        
        #Commit to database
        self.conn.commit()

        print("Updated ", item_id, "to become", estimate)

        return "Completed Update"
    
    def get_times(self):
        '''Return all the items and times in the database as a dictionary'''
        #connect to the database
        c = self.conn.cursor()  

        #Get all items
        results = c.execute('''SELECT item_id, estimate FROM Times;''').fetchall()

        #Add all items as a dictionary id:time
        obj = {}
        for x in results:
            obj[x[0]] = x[1]

        self.conn.commit() # commit commands

        print("Returned existing times")

        return obj
