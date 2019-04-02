#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

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
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    now = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    tomorrow = datetime.datetime.utcnow().replace(hour=0,minute=0,second=0,microsecond=0) + datetime.timedelta(days=1)
    tomorrow = tomorrow.isoformat() + 'Z'
    events_result = service.events().list(calendarId='s8hos5mvbudjmnj34b726nm8lc@group.calendar.google.com',
                                        maxResults=100, singleEvents=True,
                                        orderBy='startTime',q="소소클래스",showDeleted=True).execute()
    events = events_result.get('items', [])
    print(datetime.datetime.now())
    if not events:
        print('No upcoming events found.')
        exit(0)
    for event in events:
        #print(event)
        if event['status'] == 'cancelled':
            id = event['id']
            try:
                title = event['summary']
            except KeyError:
                continue
            print("삭제된 일정 : {}".format(title))
            for i in range(0,12):
                try:
                    service.events().delete(calendarId='qb2gfb6okeeob5s2qoh3hbiuj0@group.calendar.google.com',
                                            eventId='{0}{1}'.format(id,i)).execute()
                    print('삭제중 {}'.format(event['summary']))
                except:
                    pass

if __name__ == '__main__':
    main()

