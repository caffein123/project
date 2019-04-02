#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import requests
import pytz
from dateutil import tz
import rfc3339
tzinfo = tz.gettz('UTC')


event_id = []
sender_list = []
description = []
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def get_video_urls(start_convert,end_convert,video_num,location):
    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    weekday = start_convert.weekday()
    video_urls = {
	
    }
    video_url = "".join(video_urls.get(str(video_num)))
    #print(start_convert)
    #print(video_url)
    return video_url

def send_message(title,sender_list,sender_lists,start_noti,video_url):
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    key = 'key=' + ''
    user_id = 'user_id=' + ''
    sender = 'sender=' + ''
    receiver = 'receiver=' + sender_lists
    rdate = 'rdate=' + str(start_noti.strftime("%Y%m%d"))
    rtime = 'rtime=' + str(start_noti.strftime("%H")) + str(start_noti.strftime("%M"))
    print('> '+title)
    for sender in sender_list:
        print('{0} 님에게 {1} {2}시 {3}분'.format(str(sender),start_noti.strftime("%Y%m%d"),start_noti.strftime("%H"),str(start_noti.strftime("%M"))))
    msg = 'msg=' + str(video_url)

    r = requests.post('http://apis.aligo.in/send?' + key + '&' + user_id + '&' + sender + '&' + receiver + '&' + msg + '&' + rdate + '&' + rtime,
                      json=[], headers=headers)
    # print(r.elapsed.total_seconds())
    # print(r.headers)
    return r.json()

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
    now = rfc3339.rfc3339(datetime.date.today())
    tomorrow = rfc3339.rfc3339(datetime.date.today() + datetime.timedelta(1))
    events_result = service.events().list(calendarId='qb2gfb6okeeob5s2qoh3hbiuj0@group.calendar.google.com',
                                        maxResults=100, singleEvents=True, timeMin=now, timeMax=tomorrow,
                                        orderBy='startTime',q="미전달",timeZone="Asia/Seoul",showDeleted=False).execute()
    events = events_result.get('items', [])
    print(datetime.datetime.now())
    if not events:
        print('No upcoming events found.')
        exit(0)
    for event in events:
        event_id = []
        sender_list = []
        description = []
        event_id = event['id']
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        location = event['location']
        try:
            start_noti = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S+09:00')
            end_noti = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S+09:00')
            start_convert = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S+09:00') + datetime.timedelta(days=3)
            end_convert = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S+09:00') + datetime.timedelta(days=3)
        except ValueError:
            start_noti = datetime.datetime.strptime(start, '%Y-%m-%d')
            end_noti = datetime.datetime.strptime(end, '%Y-%m-%d')
            start_convert = datetime.datetime.strptime(start, '%Y-%m-%d') + datetime.timedelta(days=3)
            end_convert = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=3)
            pass
        title = event['summary']
        ori_title = str(title).split('~')[0]
        video_send_result =str(title).split('~')[2]
        video_num = str(title).split('~')[1]
        video_url = get_video_urls(start_convert,end_convert,video_num,location)
        if video_url == None:
            raise Exception('Null url')
            pass
        else:
            description = event['description']
            students_inform = str(description).split('\n')
            for student in students_inform:
                sender_list.append(student.split(',')[1])
        sender_lists= ",".join(sender_list)
        send_result = send_message(title,sender_list,sender_lists, start_noti,video_url)
        if send_result['result_code'] == '1':
            event = service.events().get(calendarId='qb2gfb6okeeob5s2qoh3hbiuj0@group.calendar.google.com', eventId=event_id).execute()
            video_send_result = '전달'
            event['summary'] = ori_title+'~'+video_num+'~'+video_send_result
            updated_event = service.events().update(calendarId='qb2gfb6okeeob5s2qoh3hbiuj0@group.calendar.google.com', eventId=event_id, body=event).execute()
            #print(updated_event['updated'])
        elif send_result['result_code'] == -115:
            pass
        else:
            event = service.events().get(calendarId='qb2gfb6okeeob5s2qoh3hbiuj0@group.calendar.google.com', eventId=event_id).execute()
            video_send_result = '비정상'
            event['summary'] = ori_title + '~' + video_num + '~' + video_send_result
            updated_event = service.events().update(calendarId='qb2gfb6okeeob5s2qoh3hbiuj0@group.calendar.google.com', eventId=event_id, body=event).execute()
            #print(updated_event['updated'])
        print(send_result['message'])

if __name__ == '__main__':
    main()

