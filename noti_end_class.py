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
import sys
tzinfo = tz.gettz('UTC')


event_id = []
sender_list = []
description = []
eventId = sys.argv[1]
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def get_video_urls(start_convert,end_convert,video_num,location):
    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    weekday = start_convert.weekday()
    video_urls = {
	 "0": ['소소클래스 오프라인수업 사전공지\n',
                '\n', '안녕하세요 소소입니다 : )\n',
                '\n', '한달동안 함께 할 소소영상클래스 수업방식과 준비물에 대해 간단하게 설명드릴게요~\n',
                '꼼꼼히 숙지하신 후 참여하셔야 합니다.\n', '\n',
                '▶ 수업방식\n', '오프라인1  온라인10\n',
                '\n', '오프라인 수업이 끝난 후, 온라인으로 계속되는 한달동안 3일에 한 번 영상 강의를 보내드릴거고 3일마다 1개의 영상을 만들어보는 미션도 주어질거에요!\n',
                '\n', '주어지는 10번의 미션, 모두 완료시 보증금(3만원)은 환불해드립니다!\n', '미션은 카페에 업로드 하신 날짜로 책정됩니다. \n',
                '\n', '영상 만드시면서 자유롭게 질문과 답변 주고 받는, ‘함께’하는 스터디입니다.\n', '\n', '▶ 시간과 장소\n',
                '{0}년 {1}월 {2}일 {3}요일 {4}:{5}-{6}:{7}\n'.format(start_convert.year,start_convert.month, start_convert.day,weekdays[weekday],start_convert.hour,start_convert.strftime("%M"),end_convert.hour,end_convert.strftime("%M")),
                '{0}\n'.format(location), '\n', '\n', '▶ 준비물\n', '\n', "1. 어도비 '프리미어 프로CC2019'가 설치된 노트북\n", '\n',
                '월 2만원대 유료 결제 프로그램입니다. \n', '- 일주일 무료체험이 가능하기 때문에 오프라인 수업시간에는 체험판만 설치해오셔도 무방합니다. \n',
                '- 꼭 아래의 경로를 이용해 설치해주세요. 다른 버전 설치시 수업내용과 다를 수 있음을 알려드립니다. \n', '\n', '프리미어 설치경로 :\n',
                'https://www.adobe.com/kr/products/premiere.html\n', '상단 무료체험판 다운로드 후 결제\n',
                '\n', '간혹 수업시간에 여러 문제가 발생하는 경우가 많아 설치 후 꼭 실행해보실 것을 당부드립니다. \n', '실행방법 : 시작메뉴 > premiere pro 검색 후 실행\n',
                '\n', '\n', '2. 함께 편집해 볼 영상, 사진, 음악 등 종류별로 여러가지 컴퓨터에 넣어 수업에 참여해주세요. 자신의 영상을 제작해야 더 흥미롭게 작업할 수 있으므로 별도의 소스제공은 해드리지 않습니다. \n',
                '\n', '3. 이어폰도 함께 지참해주시면 좋아요\n', '\n', '▶ 문의사항\n', '질문은 유튜브홀릭 카페 ‘QnA’게시판을 통해 자유롭게 궁금한 점 물어보시면 답변드리겠습니다. \n',
                'http://cafe.naver.com/vixx\n', '\n', '*\n', '주고 받은 대화는 모자이크(익명) 처리 후 추후 강의 홍보용으로 쓰일 수 있습니다. \n', '\n', 'ㅡ\n', '궁금하신 점은 언제든지 문자주세요 : )'],
    }
    video_url = "".join(video_urls.get(str(video_num)))
    #print(start_convert)
    #print(video_url)
    return video_url

def send_message(title,sender_list,sender_lists,start_noti,video_url):
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    key = 'key=' + 'lgkuh9hebk2xwyamwrd0qvj3p7e0gs99'
    user_id = 'user_id=' + 'caffein123'
    sender = 'sender=' + '01094908958'
    receiver = 'receiver=' + sender_lists
    rdate = 'rdate=' + str(start_noti.strftime("%Y%m%d"))
    rtime = 'rtime=' + str(start_noti.strftime("%H")) + str(start_noti.strftime("%M"))
    print('> '+title)
    for sender in sender_list:
        print('{0} 님에게 문자를 전송하였습니다.'.format(str(sender)))
    msg = 'msg=' + str(video_url)

    r = requests.post('http://apis.aligo.in/send?' + key + '&' + user_id + '&' + sender + '&' + receiver + '&' + msg,
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
    eventId = sys.argv[1]
    event = service.events().get(calendarId='s8hos5mvbudjmnj34b726nm8lc@group.calendar.google.com',
                                 eventId=eventId).execute()
    print(datetime.datetime.now())
    if not event:
        print('No upcoming events found.')
        exit(0)
    sender_list = []
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    location = event['location']
    try:
        start_noti = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S+09:00')
        start_convert = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S+09:00')
        end_convert = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S+09:00')
    except ValueError:
        start_noti = datetime.datetime.strptime(start, '%Y-%m-%d')
        start_convert = datetime.datetime.strptime(start, '%Y-%m-%d') + datetime.timedelta
        end_convert = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta
        pass
    title = event['summary']
    video_num = "0"
    video_url = get_video_urls(start_convert,end_convert,video_num,location)
    if video_url == None:
        raise Exception('Null url')
        exit(0)
    else:
        description = event['description']
        students_inform = str(description).split('\n')
        for student in students_inform:
            sender_list.append(student.split(',')[1])
    sender_lists= ",".join(sender_list)
    send_result = send_message(title,sender_list,sender_lists, start_noti,video_url)
    print(send_result['message'])

if __name__ == '__main__':
    main()


