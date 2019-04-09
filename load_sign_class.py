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
    events_list = []
    cal_list = ['eunsstudio@gmail.com','8tfjs65cgvgcb4ipefp2v8ne94@group.calendar.google.com','se914adb96ju93t3ef7m1vgq5c@group.calendar.google.com']
    for cal_id in cal_list:
        events_result = service.events().list(calendarId=cal_id,
                                        maxResults=100, singleEvents=True,
                                        orderBy='startTime',q="소소클래스",showDeleted=False).execute()
        for event in events_result['items']:
            events_list.append(event)
    dict_lists =[]
    for event in events_list:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S+09:00')
        start_time = start_time.strftime("%Y-%m-%d %H:%M")
        dict_lists.append({"{}-{}".format(event['summary'], start_time): event['id']})
    json_data_list = json.dumps(dict_lists, ensure_ascii=False)
    print(json_data_list)

if __name__ == '__main__':
    main()

