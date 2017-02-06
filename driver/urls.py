from django.conf.urls import url

from . import views

app_name = 'driver'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    # play blip sound
    url(r'^blip/$', views.blip, name='blip'),
    
    # sensors display
    url(r'^sensors/$', views.sensors, name='sensors'),
    
    
    url(r'^furnacework/$', views.furnacework, name='furnacework'),
    
    #inroom
    url(r'^inroom/$', views.inroom, name='inroom'),
    #onfurnace
    url(r'^onfurnace/$', views.onfurnace, name='onfurnace'),
    
    #usertemp
    url(r'^usertemp/$', views.usertemp, name='usertemp'),
    
    #workpercent
    url(r'^workpercent/$', views.workpercent, name='workpercent'),
]
