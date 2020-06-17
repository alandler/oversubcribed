print("hello")

from datetime import datetime
import todoist
import sqlite3
import requests

db = 'data.db' #[Item ID, Project ID, Content, Due Date, Priority, Time Estmate]

#access database and table
conn = sqlite3.connect(db) 
c = conn.cursor()  
c.execute('''CREATE TABLE IF NOT EXISTS timetable (item_id real PRIMARY KEY, project_id real, content text, due_date timestamp, priority real, time_estimate real);''')


api = todoist.TodoistAPI('f84b92c505121b40a3489b4904b7eeb99ad11b7b')
api.sync()

def request_handler(request):
    update_database()

    return "Enter request handler"

    if request['method'] == 'GET':
        return "Enter get handler"
        entries = c.execute('''SELECT item_id, project_id, content, due_date, priority, time_estimate,  FROM timetable''').fetchall()
        return entries

def get_projects_and_items(api):
    '''Get projects and items as lists of such items, for simplicity'''
    projects = api.state['projects']
    items = api.state['items']
    return projects, items

def set_project_item_name_id_dicts(api, projects, items):
    '''Map the projects and tasks to their ids'''
    projects_name_id_dict = {}
    items_name_id_dict = {}

    for project in projects:
        projects_name_id_dict[project['name']] = project['id']

    for item in items:
        items_name_id_dict[item['content']] = item['id']

    return projects_name_id_dict, items_name_id_dict

def list_current_items(api, items):
    current_items = []

    for item in items:
        if item['checked'] == 0 and item['is_deleted'] == 0:
            current_items.append(item)

    return current_items

def item_time_estimates(api, current_items):
    '''Create a diciontary mapping item names to time estimates'''
    item_time_estimates = {}

    for item in current_items:
        if item not in item_time_estimates:
            print("Estimate time for: ", item['content'])
            temp_time_estimate = input()
            #Handle inputs of form 1h30m and also just 1h or just 30m
            index = 0
            hour_count = ''
            minute_count = ''

            if 'h' in temp_time_estimate:
                while temp_time_estimate[index] != 'h':
                    hour_count = hour_count+temp_time_estimate[index]
                    index+=1
            if 'm' in temp_time_estimate:
                while temp_time_estimate[index] != 'm':
                    hour_count = hour_count+temp_time_estimate[index]
                    index+=1
            
            estimate_as_hours = 0

            if hour_count != '':
                estimate_as_hours += float(hour_count)
            if minute_count != '':
                estimate_as_hours += round(float(minute_count)/60, 2)
            

            item_time_estimates[item['content']] = estimate_as_hours
    return item_time_estimates

def project_time_estimates(api, items, item_time_estimates):
    '''Create dictionary mapping project __ID!!!__ to time estimates'''
    project_time_estimates = {}

    for item in items:
        temp_project_id = item['project_id']
        if temp_project_id in project_time_estimates:
            project_time_estimates[temp_project_id] += item_time_estimates[item['content']]
        else:
            project_time_estimates[temp_project_id] = item_time_estimates[item['content']]

    return project_time_estimates

def create_set_of_today_items(api, items):
    '''Create set of today items

    MUST HANDLE ALL FORMATS:
    Full-day dates (like “1 January 2018” or “tomorrow”)
    Floating due dates with time (like “1 January 2018 at 12:00” or “tomorrow at 10am”)
    Due dates with time and fixed timezone (like “1 January 2018 at 12:00 America/Chicago” or “tomorrow at 10am Asia/Jakarta”)

    Date object['date'] = "2016-12-0T12:00:00" for example
    '''
    today_item_set = set()

    today = datetime.today()
    today = today.strftime("%Y-%m-%d")

    for item in items:
        if item['due']['date'][:len(today)] == today or item['due']['date'] == today[:len(today)-1] + "T":
            today_item_set.add(item)

    return today_item_set

def get_today_hours(api, today_item_set):
    '''
    Using the set of today items from create_set_of_today_items and hour counts from item_time_estimates
    tabulate the hour counts for all the day
    '''
    pass
    #for item in today_item_set:
        #if

#print(get_projects_and_items(api))
def update_database():
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

update_database()
        

conn.close()