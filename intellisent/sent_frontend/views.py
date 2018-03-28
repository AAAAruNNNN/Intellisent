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

def index(request):
    return render(request, 'sent_frontend/index.html')

def channels(request):
    channel_list = Channel.objects.all()
    
    context = {'channel_list': channel_list}
    return render(request, 'sent_frontend/channels.html', context)

def programs(request, cid):
    c = get_object_or_404(Channel, pk=cid)
    
    current_time = datetime.now()
    three_days_ago = datetime.now() - timedelta(days=1)

    endtime = str(current_time.year) + \
            "{:02d}".format(current_time.month) + \
            "{:02d}".format(current_time.day) + \
            "{:02d}".format(current_time.hour) + \
            "{:02d}".format(current_time.minute)

    starttime = str(three_days_ago.year) + \
            "{:02d}".format(three_days_ago.month) + \
            "{:02d}".format(three_days_ago.day) + \
            "{:02d}".format(three_days_ago.hour) + \
            "{:02d}".format(three_days_ago.minute)        

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
            if not Program.objects.filter(program_id = episode['programmeid']).count():
                p = Program(channel = Channel.objects.get(channel_id=episode['channelid']),
                    program_id = episode['programmeid'],
                    name = episode['title'],
                    image = episode['programmeurl'],
                    genre = episode['subgenre'],
                    duration = episode['duration'])
                p.save()
    except Exception as e:
        print("THERE WAS NO ERROR DURING SCRAPE\n" + str(e))
        
    c_programs = Program.objects.filter(channel=c)

    context = {'channel' : c, 'programs': c_programs}
    return render(request, 'sent_frontend/programs.html', context)


def episodes(request, cid, sid):

    s = get_object_or_404(Program, pk=sid)
    c = get_object_or_404(Channel, pk=cid)

    s_episodes = Episode.objects.filter(program=s)

    context = {'show': s, 'episodes': s_episodes, 'channel': c}
    return render(request, 'sent_frontend/episodes.html', context)

def episode_sentiment(request, cid, sid, eid):
    c = get_object_or_404(Channel, pk=cid)
    s = get_object_or_404(Program, pk=sid)
    e = get_object_or_404(Episode, pk=eid)

    


    context = {'episode': e, 'show': s, 'channel': c}
    return render(request, 'sent_frontend/episode_sentiment.html', context)