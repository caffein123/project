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
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    now = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    tomorrow = datetime.datetime.utcnow().replace(hour=0,minute=0,second=0,microsecond=0) + datetime.timedelta(days=1)
    tomorrow = tomorrow.isoformat() + 'Z'
    events_result = service.events().list(calendarId='uu1pujll7gnpdqvj5bfbo9bh34@group.calendar.google.com',
                                        maxResults=100, singleEvents=True,
                                        orderBy='updated',showDeleted=False).execute()

    dict_lists = []
    for event in events_result['items']:
        id = event['id']
        user = event['description'] + "(입금)"
        dict_lists.append({user:id})
    json_data_list = json.dumps(dict_lists, ensure_ascii=False)
    print(json_data_list)

if __name__ == '__main__':
    main()

