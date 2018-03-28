from django.urls import path

from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.index, name='index'),
    path('channels', views.channels, name='channels'),
    path('channel/<int:cid>', views.programs, name='programs'),
    path('channel/<int:cid>/show/<int:sid>', views.episodes, name='episodes'),
    path('channel/<int:cid>/show/<int:sid>/episode/<int:eid>', views.episode_sentiment , name='episode_sentiment')
]