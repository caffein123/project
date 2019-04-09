#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def create_event(id_insert,title,description,start_convert,end_convert,color,location):
    event_body = {
        'id' : id_insert,
        'summary': title,
        'description': description,
        'colorId' : color,
        'location' : location,
        'start': {
            'dateTime': start_convert,
            'timeZone': 'Asia/Seoul',
        },
        'end': {
            'dateTime': end_convert,
            'timeZone': 'Asia/Seoul',
        }
    }
    return event_body

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('/home/soso/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/home/soso/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    now = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    tomorrow = datetime.datetime.utcnow().replace(hour=0,minute=0,second=0,microsecond=0) + datetime.timedelta(days=1)
    tomorrow = tomorrow.isoformat() + 'Z'
    events_result = service.events().list(calendarId='s8hos5mvbudjmnj34b726nm8lc@group.calendar.google.com',
                                        maxResults=100, singleEvents=True,
                                        orderBy='startTime',q="소소클래스",showDeleted=False).execute()
    dict_lists = []
    for event in events_result['items']:
     start_time = event['start'].get('dateTime', event['start'].get('date'))
     start_time = datetime.datetime.strptime(start_time , '%Y-%m-%dT%H:%M:%S+09:00')
     start_time = start_time.strftime("%Y-%m-%d %H:%M")

     dict_lists.append({ "{}-{}".format(event['summary'],start_time):event['id'] })
    json_data_list = json.dumps(dict_lists,ensure_ascii = False)
    print(json_data_list)
    #events = events_result.get('items', [])
    #if not events:
        #exit(0)
    #for event in events['items']:
    	#print(events['summary'])

if __name__ == '__main__':
    main()
