#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
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
    eventId = sys.argv[1]
    event = service.events().get(calendarId='s8hos5mvbudjmnj34b726nm8lc@group.calendar.google.com',
                                 eventId=eventId).execute()
    print(datetime.datetime.now())
    if not event:
        print('No upcoming events found.')
        exit(0)
    id = event['id']
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    title = event['summary']
    print("> "+title)
    description = event['description']
    location = event['location']
    for i in range(0,12):
        event_vedio = service.events().get(calendarId='qb2gfb6okeeob5s2qoh3hbiuj0@group.calendar.google.com',
                                               eventId='{0}{1}'.format(id,i)).execute()
        title_video = event_vedio['summary']
        title_video = str(title_video).split('~')
        event_vedio['description'] = description
        event_vedio['location'] = location
        if i == 0:
            event_vedio['summary'] = title + ' [사전공지]~' + title_video[1] + '~' + title_video[2]
            try:
                start_convert = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S+09:00') + datetime.timedelta(
                        days=-3)
                end_convert = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S+09:00') + datetime.timedelta(days=-3)
            except ValueError:
                start_convert = datetime.datetime.strptime(start, '%Y-%m-%d') + datetime.timedelta(days=-3)
                end_convert = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=-3)
                pass
        else:
            if i == 11:
                event_vedio['summary'] = title + ' [마지막공지]~' + title_video[1] + '~' + title_video[2]
            else:
                event_vedio['summary'] = title + '~' + title_video[1] + '~' + title_video[2]
            try:
                start_convert = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S+09:00') + datetime.timedelta(days=i*3)
                end_convert = end_convert = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S+09:00') + datetime.timedelta(days=i*3)
            except ValueError:
                start_convert = datetime.datetime.strptime(start, '%Y-%m-%d') + datetime.timedelta(days=i*3)
                end_convert = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=i*3)
                pass
        start_convert = start_convert.isoformat() + '+09:00'
        end_convert = end_convert.isoformat() + '+09:00'
        event_vedio['start']['dateTime'] = start_convert
        event_vedio['end']['dateTime'] = end_convert
        updated_event = service.events().update(calendarId='qb2gfb6okeeob5s2qoh3hbiuj0@group.calendar.google.com',
                                                eventId='{0}{1}'.format(id,i), body=event_vedio).execute()
        print('{0} : 업데이트 완료'.format(updated_event['summary']))

if __name__ == '__main__':
    main()

