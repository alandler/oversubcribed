from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service 

def get_next_n_events(service,n):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    return events

def get_calendars(service):
    '''Get list of calendars on a user's gcal account'''
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print(calendar_list_entry['summary'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    print(calendar_list.keys())
    return calendar_list

def get_upcoming_events_today(service):
    '''Get all events for today'''
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print("NOW: ", now)
    latest_today = datetime.datetime.combine(datetime.date.today(),datetime.time(12,59,59,999999))
    print('Getting the events for today')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax = latest_today,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def get_all_events_on_day(service, day):
    #Check if object, if not convert
    #same as above
    raise NotImplementedError

def convert_date_format(input):
    '''Take in input MM/DD/YYYY return y,m,d'''
    month = int(input[:2])
    day = int(input[3:5])
    year = int(input[6:10])

    return year, month, day

def get_early_time(y,m=None,d=None):
    if m==None:
        combined = datetime.datetime.combine(y, datetime.time(0,0,0))
        combined = combined.replace(tzinfo=pytz.UTC)
        return combined.isoformat()
    else:    
        return datetime.datetime(y,m,d,0,0,0,tzinfo = datetime.timezone.utc).isoformat()

def get_late_time(y,m=None,d=None):
    if m==None:
        combined = datetime.datetime.combine(y, datetime.time(12,59,59,999999))
        combined = combined.replace(tzinfo=pytz.UTC)
        return combined.isoformat()
    else:    
        return datetime.datetime(y,m,d,12,59,59,999999,tzinfo = datetime.timezone.utc).isoformat()

        


if __name__ == '__main__':
    service = main()
    get_next_n_events(service, 10)
    get_calendars(service)
    get_upcoming_events_today(service)
    