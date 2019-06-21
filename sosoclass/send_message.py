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
	"1": ['1강 영상만들기 AtoZ\n',
              '\n', '안녕하세요 소소입니다 ^^\n',
              '우리 오프라인 수업 때 들었던 \n',
              '프리미어로 영상 만드는 법 처음부터 끝까지!\n',
              '영상만드는 방법을 쭉 훑어주는 시간이에요.\n',
              '\n', '1강 온라인강의\n',
              'http://sosoclass.com/4396\n',
              '\n', '전체요약본 PDF\n',
              'http://sosoclass.com/2737\n',
              '\n', '위의 영상과 아래 PDF를 보면서\n',
              '함께 차근차근 하나씩 해나가시다보면\n',
              '영상 하나가 뚝딱! 만들어져 있을거에요 ♡ \n',
              '\n', '파일로 출력해서 만들어 드리고 싶었으나 제가 미니멀라이프를 실천하면서 지구를 위해 무분별한 종이의 사용을 줄이고 있습니다 ^^\n',
              'PDF 디지털 파일로 드리는 점, 양해부탁드립니다. \n',
              '하지만! 잃어버릴 염려도 없고! 언제 어디서나 꺼내 볼 수 있는 장점이 있으니까요, 더욱 좋으실 거에요♡ \n',
              '\n',
              '\n', '- 1차미션은 ‘소소클래스VLOG’라는 주제로 진행되지만 2차미션부터는 본인이 원하는 방향대로 영상을 제작하시면 됩니다!\n',
              '\n', '- 10개 미션 중 7개의 미션을 성공하시면 \n',
              '보증금을 환급해 드립니다\n',
              '\n',
              '\n', '1차미션  |  {0}월 {1}일, 카페 게시글 기준\n'.format(start_convert.month, start_convert.day),
              '\n', '소소영상클래스, 하루동안 있었던 일을\n',
              'VLOG로 제작해보세요 ^_^ \n',
              '다른 주제도 뭐든 좋아요\n',
              '하시면서 모르시는 것들은 언제든 카톡남겨주세요\n',
              ':\n', '유튜브홀릭카페\n',
              '공부해요 > 미션제출 게시판 업로드\n', 'http://cafe.naver.com/vixx\n',
              '\n', '가입인사, 등업신청에 소소클래스 언급해주시면 최고등급으로 등업됩니다- ♡ \n',
              '\n', 'ㅡ\n',
              'SOSOCLASS 1'],
        "2": ['2강, 나도 유튜버!\n',
              '유튜브 채널을 만들어보자!\n',
              'http://sosoclass.com/9898\n',
              '\n', '두번째 미션은 유튜브 채널을 개설하고\n',
              '‘동영상 업로드’를 해보는 거에요 ^~^\n',
              '프로필 설정도 하고 채널아트, 재생목록도 만들어봅시다!\n',
              '\n', '2차미션  | {0}월 {1}일, 카페 게시글 기준\n'.format(start_convert.month, start_convert.day),
              '\n', '자신이 만든 유튜브 영상 URL을 포함해 \n',
              '유튜브 채널을 소개해주세요!\n',
              ':\n', '유튜브홀릭카페\n',
              '등업해요 > 내채널소개 게시판 업로드\n',
              'http://cafe.naver.com/vixx\n',
              '\n', 'ㅡ\n', 'SOSOCLASS 2\n',
              '\n',
              '\n', '자신의 채널을 만들고 소개 해주시면 됩니다! \n',
              '\n', '여유로우시다면 영상을 또 만드셔서 올리시면 너무 좋고요, \n',
              '그렇지 않으신 분들은 1강에서 만들었던 영상 업로드 한 후 소개해주셔도 좋아요 : )\n',
              '\n', '\n', '> 채널아트 디자인하는 방법 URL\n', 'https://cafe.naver.com/vixx/8821'],
        "3": ['3강, 시퀀스만들기\n',
              '\n', '오프라인수업이 끝난 후 \n',
              '일주일 동안 가장 많이 질문주셨던 \n',
              '어려우시고 헷갈리실 수 있는\n',
              '시퀀스 만드는 방법이에요~\n',
              '\n', 'http://sosoclass.com/6832\n',
              '\n', '프로젝트가 스케치북이였다면\n',
              '시퀀스는 스케치북 속 종이에요. \n',
              '궁금증이 조금은 풀리시길 바라며 ^^\n', '\n', '\n',
              '3차미션 | {0}월 {1}일, 카페 게시글 기준\n'.format(start_convert.month, start_convert.day), '\n',
              '보편적인 가로영상, 조금 특별한 세로영상,\n',
              '1:1 비율의 인스타그램용 등\n',
              '본인에게 필요한 영상도 만들어보세요~\n',
              ':\n', '유튜브홀릭카페\n', '공부해요 > 미션제출 게시판 업로드\n',
              'http://cafe.naver.com/vixx\n', '\n', '\n', 'ㅡ\n', 'SOSOCLASS 3'],
        "4": ['4강, 좀 더 쉽고 빠르게 편집을 - 후다닥!\n',
              '\n', '\n', '조금은 귀찮고 번거로운 편집을\n',
              '단축키로 수월하게 할 수 있는 방법을 알려드렸어요 ^^\n',
              '\n', '강의 시간은 길지만\n', '이 20분이라는 시간 할애해서\n',
              '앞으로 몇 시간을 단축시킬 수 있다면 결코 헛 된 시간은 아니겠죠~?\n',
              '\n', 'http://sosoclass.com/5689\n', '\n', '처음엔 익숙하지 않아서 불편할 수도 있는 단축키여도\n',
              '꾸준히 연습하신다면 아마 정말 편리한 기능들이 될거에요. \n', '\n', '+ 더불어 강의 중간에 달달한 특별미션! \n',
              "가장 먼저 '정답'을 외쳐주신분께 행운이 있을거에요\n", '\n', '\n', '\n',
              '4차미션 | {0}월 {1}일 카페게시글기준\n'.format(start_convert.month, start_convert.day),
              '\n', '4개 이상의 다양한 영상을 활용해서 다채로운 영상으로 편집하기!\n',
              '유튜브에 업로드하고 게시판에 소개해주시면 됩니다~\n', ':\n', '유튜브홀릭카페\n',
              '공부해요 > 미션제출 게시판 업로드\n', 'http://cafe.naver.com/vixx\n', '\n', '\n', 'ㅡ\n', 'SOSOCLASS 4'],
        "5": ['5강, 밝고 선명한, 아름다운 영상을 위하여\n',
              '\n', '기껏 촬영한 영상이, 사진이 어두컴컴하고 칙칙하고..\n',
              '내 맘 같지 않게 나오셨나요?\n', '그렇다구 영상 만들기를 포기할 순 없죠!\n',
              '\n', 'http://sosoclass.com/2880\n', '\n', '영상을 밝게하거나 어둡게,\n',
              '더 선명하고 예쁜 색감으로 바꾸는 방법을 알려드리려고 해요\n', '이런 과정을 ‘영상을 보정한다’고 하는데요, \n',
              '우리가 흔히 보는 드라마 영화에서도 색감보정은 필수랍니다!\n', '아주 간단하게! 영상보정할 수 있는 방법을 알려드릴게요\n',
              '\n', "+ 더불어 '필터' 영상강의도 함께해보세요~\n", 'https://cafe.naver.com/vixx/8445\n', '\n', '\n',
              '5차미션 | {0}월 {1}일, 카페 게시글 기준\n'.format(start_convert.month, start_convert.day), '\n',
              '내 영상을 밝게, 또는 영화처럼 \n',
              '자신의 스타일에 맞게 보정해보세요\n', ':\n', '유튜브홀릭카페\n', '공부해요 > 미션제출 게시판 업로드\n',
              'http://cafe.naver.com/vixx\n', '\n', 'ㅡ\n', 'SOSOCLASS 5'],
        "6": ['6강, 자막을 넣어볼까?\n',
              '\n', '영상만들기 A to Z 강의에서 먼저 알려드렸던 자막넣기.\n',
              '영상을 만드시다 보니까 여러가지 어려움에 부딪히셨죠? 더 깔끔하고 잘 어울리는 자막과 아이콘을 넣어 꾸미고 싶은데 마음처럼 쉽지 않아 포기하진 않으셨나요! \n',
              '\n', 'http://sosoclass.com/1756\n',
              '\n', '쉽게 자막넣는 방법, 더 자세하게 알려드렸으니까요!\n', '아마 한층 더 재밌게 영상 만드실 수 있을거에요~\n',
              '\n', '강의 보시고도 풀리지 않은 실마리가 있으시다면,\n', '언제든지 카톡주세요 ^^\n', '\n', '그럼 이번에도 굿럭!\n',
              '\n', '\n', '\n', '6차미션 | {0}월 {1}일, 카페 게시글 기준\n'.format(start_convert.month, start_convert.day), '\n',
              '색, 외곽선, 그림자 등을 사용하여\n',
              '상황에 어울리는 여러 스타일의 자막을 넣어 \n', '영상 완성하기!\n', '\n', '유튜브홀릭카페\n',
              '공부해요 > 미션제출 게시판 업로드\n', 'http://cafe.naver.com/vixx\n', '\n', '\n', 'ㅡ\n', 'SOSOCLASS 6'],
        "7": ['7강, 음악이필요해\n',
              '\n', '안녕하세요~ 벌써 7강이에요! ㅎㅎ\n',
              '시간 무척빠르죠 ㅠㅠ\n', '\n', '이번 강의에서는 \n', '음악을 검색하고 다운로드 받는 방법, \n',
              '저작권 무료 음원에 대해 알려드렸어요 ^^\n', '\n', '중간중간 애니메이션하는 방법, \n', '편집속도를 빠르게 해주는\n',
              '깨알팁들도 숨어 있으니 \n', '찬찬히 여유롭게 보세요 ^-^\n', '\n', '영상강의 시간이 20분이 넘어가면\n',
              '집중도가 흐려지는거 너무나도 잘 알아요 ㅎㅎ\n', '1, 2편으로 나누어 준비해보았으니\n',
              '효과음 관련해서는 3일 뒤, 8강에서 만나요!\n', '\n', 'http://sosoclass.com/3145\n', '\n',
              '이번엔 자신의 영상에 \n', '어울리는 음악을 다운 받으셔서 \n', '좋은 음악과 영상이 공존하는 콘텐츠 \n',
              '한 번 제작해 볼까요?\n', '\n', '\n', '\n',
              '7차미션 | {0}월 {1}일 카페 게시글 기준\n'.format(start_convert.month, start_convert.day), '\n',
              '내 영상에 어울리는 음악을 찾아 다운 받아 \n', '배경음악으로 쓰인 콘텐츠 만들기!\n', '+ 더보기란에도 정보 기입 잊지 말기!\n',
              '\n', '바쁘시더라도! \n', '단10초짜리 짧은 영상이라도 만들어봐요~ \n', '소중한 시간내어 열심히 배운거 잊어버리지 않게 \n',
              '우리 미션 달성해서 수강료 꼭 환급받아요 ㅋ_ㅋ\n', ':\n', '유튜브홀릭카페\n', '공부해요 > 미션제출 게시판 업로드\n',
              'http://cafe.naver.com/vixx\n', '\n', '\n', 'ㅡ\n', 'SOSOCLASS 7'],
        "8": ['8강, 효과음\n', '\n', '저번 배경음악 강의에 이어\n', '이번 시간엔 ‘효과음’에 관련한 것들을 알려드렸어요.\n',
              '\n', '효과음을 더욱 효과적으로 \n', '넣을 수 있는 방법부터\n', '\n', '유튜브영상 다운로드하는 방법\n',
              '영상이나 음악을 묶을 수 있는 NEST \n', '영상 흔들림 보정하는 Warp Stabilizer\n', '음향 적정 레벨 등\n',
              '다양한 꿀팁들이 숨어있어요\n', '\n', 'http://sosoclass.com/5292\n', '\n', '\n', '\n', '\n',
              '8차미션 | {0}월 {1}일, 카페 게시글 기준\n'.format(start_convert.month, start_convert.day),
              '\n', '그동안 다소 밋밋한 나의 영상에\n', '적절한 효과음을 넣어\n', '더욱 풍성하게 꾸며보세요 : )\n', '\n', ':\n', '\n',
              '유튜브홀릭카페\n', '공부해요 > 미션제출 게시판 업로드\n', 'http://cafe.naver.com/vixx\n', '\n', '\n', 'ㅡ\n', 'SOSOCLASS 8'],
        "9": ['9강, 신기한 전환 효과 넣기\n', '\n', '영상과 영상사이에 신비한 일이?!\n',
              '제일 많이 쓰는 디졸브부터 밀기, \n', '페이지 넘기기 등등 재밌는 효과 넣어보기\n',
              '더불어 템플릿활용으로 \n', '편리하게 영상을 제작해보자!\n', '\n', 'http://sosoclass.com/2303\n',
              '\n', '9차미션 | {0}월 {1}일, 카페 게시글 기준\n'.format(start_convert.month, start_convert.day),
              '\n', '다양한 트랜지션 효과를 사용해서\n', '내 영상 콘텐츠의 매력을 \n',
              '더욱 극대화 할 수 있는 편집을 해보세요\n', ':\n', '유튜브홀릭카페\n',
              '공부해요 > 미션제출 게시판 업로드\n', 'http://cafe.naver.com/vixx\n', '\n', 'ㅡ\n', 'SOSOCLASS 9'],
        "10": ['10강, TIP!\n', '\n', '프리미어, 유튜브에서 \n', '유용하게 사용할 수 있는 \n', '소소한 팁들을 알려드려요 ^^\n',
              '\n', 'http://sosoclass.com/6119\n', '\n', '\n',
              '10차미션 | {0}월 {1}일, 카페 게시글 기준\n'.format(start_convert.month, start_convert.day), '\n',
              '수업후기 게시판에 소소클래스 한달간 후기와 함께\n', '지금까지 만들었던 유튜브 영상들 중\n', '가장 마음에 드는 영상 3가지를 \n',
              '블로그, 카페에 소개해주세요 ^^\n', ':\n', '유튜브홀릭카페\n', '공부해요 > 수업후기 게시판 업로드\n',
              'http://cafe.naver.com/vixx\n', '\n', '\n', 'ㅡ\n', 'SOSOCLASS 10'],
        "11": ['마지막 공지\n', '\n', '안녕하세요 : ) 소소입니다.\n',
               '\n', '오프라인에서 만나뵌지 엊그제 같은데\n', '벌써 한달이란 시간이 훌쩍지나\n',
               '클래스를 마감해야할 시간이네요..\n', '\n', '3일에 한 번 영상만드는게\n', '여간 쉬운 일이 아니죠 ~ ㅎㅎ\n',
               '바쁘셔서 아쉽게도 참여해주시지 못하셨더라도\n', '꼭 포기하지 마시고 좋은 영상, 콘텐츠 제작하시길 바랄게요 \n',
               '\n', '\n', '\n', '> 미션 성공\n', '미션 10개 중 7개 성공!\n', '제게 개인톡으로 계좌번호와 이름 남겨주세요 ^^\n',
               '확인 후 미션성공환급을 도와드리겠습니다!\n', '정말정말 수고 많으셨어요~\n', '\n', '\n', '\n', '\n', '\n', '\n',
               '> 카페 유튜브홀릭\n', 'http://cafe.naver.com/vixx\n', '\n', '이 카톡방은 이제 없어지지만\n',
               '꾸준한 습관으로 정착하길 원하신다면\n', '온라인 스터디 카페에서 만나요 : )\n', '\n', '유홀지식in 게시판에서는\n',
               '질문에 대한 답변도 해드리구요, \n', '종종 영상이나 글로 근황 전해주시면\n', '댓글로도 소통해요♡ \n', '\n', '\n',
               '\n', '\n', '한달동안 정말정말 감사했습니다.']
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

