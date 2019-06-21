#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

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
    events = events_result.get('items', [])
    print(datetime.datetime.now())
    if not events:
        print('No upcoming events found.')
        exit(0)
    for event in events:
        #print(event)
        id = event['id']
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        title = event['summary']
        try:
            location = event['location']
        except KeyError:
            print('[Error] {0} is No Value location'.format(title))
            continue
        try:
            color = event['colorId']
        except KeyError:
            color = '10'
        try:
            description = event['description']
        except KeyError:
            print('[Error] {0} is No Value description'.format(title))
            continue

        for i in range(0,12):
            event_body = {}
            id_insert = '{0}{1}'.format(id,i)
            if i == 0:
                title_insert = '{0} [사전공지]~{1}~미전달'.format(title, i)
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
                    title_insert = '{0} [마지막공지]~{1}~미전달'.format(title, i)
                else:
                    title_insert = '{0} [강의영상]~{1}~미전달'.format(title,i)
                try:
                    start_convert = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S+09:00') + datetime.timedelta(days=i*3)
                    end_convert = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S+09:00') + datetime.timedelta(days=i*3)
                except ValueError:
                    start_convert = datetime.datetime.strptime(start, '%Y-%m-%d') + datetime.timedelta(days=i*3)
                    end_convert = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=i*3)
                    pass
            start_convert = start_convert.isoformat() + '+09:00'
            end_convert = end_convert.isoformat() + '+09:00'
            try:
                event_body = create_event(id_insert,title_insert,description,start_convert,end_convert,color,location)
            except:
                pass
            try:
                event_set = service.events().insert(calendarId='qb2gfb6okeeob5s2qoh3hbiuj0@group.calendar.google.com', body=event_body).execute()
                print('생성된 일정 : {}'.format(event_set['summary']))
            except:
                print('{0} > {1} : 일정 생성 실패(이미 등록된 일정)'.format(title,title_insert))
                pass


if __name__ == '__main__':
    main()
