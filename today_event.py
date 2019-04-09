#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from dateutil import tz
import rfc3339
tzinfo = tz.gettz('UTC')
import sys

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
    date = sys.argv[1]
    date = datetime.strptime(date, '%Y-%m-%d')
    now = rfc3339.rfc3339(date)
    tomorrow = rfc3339.rfc3339(date + timedelta(1))
    #tomorrow = tomorrow.astimezone(tzinfo).isoformat()
    events_result_soso = service.events().list(calendarId='s8hos5mvbudjmnj34b726nm8lc@group.calendar.google.com', timeMin=now, timeMax=tomorrow,
                                        maxResults=100, singleEvents=True,
                                        orderBy='startTime',showDeleted=False).execute()
    events_result_video = service.events().list(calendarId='qb2gfb6okeeob5s2qoh3hbiuj0@group.calendar.google.com', timeMin=now, timeMax=tomorrow,
                                        maxResults=100, singleEvents=True,
                                        orderBy='startTime',showDeleted=False).execute()
    events_soso = events_result_soso.get('items', [])
    events_video = events_result_video.get('items', [])
    #print(datetime.now().strftime('%Y-%m-%d'))
    print('<강의 일정>')
    if not events_soso:
        print('강의 일정 없음.')
    for event_soso in events_soso:
        start_soso = event_soso['start'].get('dateTime', event_soso['start'].get('date'))
        end_soso = event_soso['end'].get('dateTime', event_soso['end'].get('date'))
        try:
            start_soso = datetime.strptime(start_soso, '%Y-%m-%dT%H:%M:%S+09:00')
            end_soso = datetime.strptime(end_soso, '%Y-%m-%dT%H:%M:%S+09:00')
            result = '{0}-{1}-{2} {3}시 {4}분 ~ {5}시 {6}분'.format(start_soso.year,start_soso.month,start_soso.day,start_soso.hour,start_soso.minute,end_soso.hour,end_soso.minute)
        except ValueError:
            start_soso = datetime.strptime(start_soso, '%Y-%m-%d')
            end_soso = datetime.strptime(end_soso, '%Y-%m-%d')
            result = '{0}-{1}-{2}'.format(start_soso.year, start_soso.month, start_soso.day)
            pass
        title_soso = event_soso['summary']
        print('> {0}'.format(title_soso))
        print('{0}'.format(result))
    print('\n<영상 배포 일정>')
    if not events_video:
        print('영상 배포 일정 없음.')
    for event_video in events_video:
        start_video = event_video['start'].get('dateTime', event_video['start'].get('date'))
        end_video = event_video['end'].get('dateTime', event_video['end'].get('date'))
        try:
            start_video = datetime.strptime(start_video, '%Y-%m-%dT%H:%M:%S+09:00')
            end_video = datetime.strptime(end_video, '%Y-%m-%dT%H:%M:%S+09:00')
            result = '{0}-{1}-{2} {3}시 {4}분 ~ {5}시 {6}분'.format(start_video.year,start_video.month,start_video.day,start_video.hour,start_video.minute,end_video.hour,end_video.minute)
        except ValueError:
            start_video = datetime.strptime(start_video, '%Y-%m-%d')
            end_video = datetime.strptime(end_video, '%Y-%m-%d')
            result = '{0}-{1}-{2}'.format(start_video.year, start_video.month, start_video.day)
            pass
        title_video = event_video['summary']
        print('> {0}'.format(title_video))
        print('{0}\n'.format(result))

if __name__ == '__main__':
    main()
