from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Channel, Program, Episode

import time
import urllib.request, json
from sent_frontend.models import Channel, Program, Episode
import requests
from time import mktime
from datetime import datetime, timedelta
import pytz
from django.utils.timezone import make_aware

def the_time(days=0):
    return datetime.now() - timedelta(days=days)

def create_time(a_time):
    return str(a_time.year) + \
        "{:02d}".format(a_time.month) + \
        "{:02d}".format(a_time.day) + \
        "{:02d}".format(a_time.hour) + \
        "{:02d}".format(a_time.minute)
     
def index(request):
    return render(request, 'sent_frontend/index.html')

def channels(request):
    channel_list = Channel.objects.all()
    
    context = {'channel_list': channel_list}
    return render(request, 'sent_frontend/channels.html', context)

def programs(request, cid):
    
    c = get_object_or_404(Channel, pk=cid)


    starttime = create_time(the_time(1))
    endtime = create_time(the_time())
    
    url = "https://timesofindia.indiatimes.com/tvschedulejson.cms?" \
    "userid=0" \
    "&channellist=" + c.name.replace(' ', '%20') + \
    "&fromdatetime=" + starttime + \
    "&todatetime=" + endtime + \
    "%20&deviceview=other&channellogo=1"
    
    try:
        data = requests.get(url).json()
        
        for episode in data['ScheduleGrid']['channel'][0]['programme']:
            if not Program.objects.filter(program_id = episode['programmeid']).count():
                p = Program(channel = Channel.objects.get(channel_id=episode['channelid']),
                    program_id = episode['programmeid'],
                    name = episode['title'],
                    image = episode['programmeurl'],
                    genre = episode['subgenre'],
                    duration = episode['duration'])
                p.save()
    except Exception as e:
        print("THERE WAS AN ERROR DURING SCRAPE\n" + str(e))
        
    c_programs = Program.objects.filter(channel=c)

    context = {'channel' : c, 'programs': c_programs}
    return render(request, 'sent_frontend/programs.html', context)

def episodes(request, cid, sid):

    s = get_object_or_404(Program, pk=sid)
    c = get_object_or_404(Channel, pk=cid)

    starttime = create_time(the_time(1))
    endtime = create_time(the_time())
    
    print(starttime)
    print(endtime)
    url = "https://timesofindia.indiatimes.com/tvschedulejson.cms?" \
    "userid=0" \
    "&channellist=" + c.name.replace(' ', '%20') + \
    "&fromdatetime=" + starttime + \
    "&todatetime=" + endtime + \
    "%20&deviceview=other&channellogo=1"
    
    print(url)
    
    try:
        data = requests.get(url).json()
        
        for episode in data['ScheduleGrid']['channel'][0]['programme']:

            startdate = time.strptime(episode['date'],'%Y%m%d')
            starttime = time.strptime(episode['start'],'%Y%m%d%H%M')
            endtime = time.strptime(episode['stop'],'%Y%m%d%H%M')
            
            startdate = datetime.fromtimestamp(mktime(startdate))
            starttime = datetime.fromtimestamp(mktime(starttime))
            endtime = datetime.fromtimestamp(mktime(endtime))

            coimbatore = pytz.timezone('Asia/Kolkata')
            
            startdate = make_aware(startdate, timezone=coimbatore)
            starttime = make_aware(starttime, timezone=coimbatore)
            endtime = make_aware(endtime, timezone=coimbatore)

            print(Episode.objects.filter(program = Program.objects.filter(program_id = episode['programmeid']).first(), program__channel = Channel.objects.filter(channel_id=episode['channelid']).first(), airtime=starttime).count())
            
            print(episode['title'])

            if not Episode.objects.filter(program = Program.objects.filter(program_id = episode['programmeid']).first(), program__channel = Channel.objects.filter(channel_id=episode['channelid']).first(), airtime=starttime).count():
                print('one episode was not there')
                e = Episode(program=Program.objects.get(program_id=episode['programmeid']),
                        airdate = startdate,
                        airtime = starttime,
                        endtime = endtime)
                e.save()
    except Exception as e:
        print("THERE WAS AN ERROR DURING SCRAPE\n" + str(e))

    s_episodes = Episode.objects.filter(program=s)

    context = {'show': s, 'episodes': s_episodes, 'channel': c}
    return render(request, 'sent_frontend/episodes.html', context)

def episode_sentiment(request, cid, sid, eid):
    c = get_object_or_404(Channel, pk=cid)
    s = get_object_or_404(Program, pk=sid)
    e = get_object_or_404(Episode, pk=eid)

    context = {'episode': e, 'show': s, 'channel': c}
    return render(request, 'sent_frontend/episode_sentiment.html', context)