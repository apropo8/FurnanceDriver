from os.path import expanduser
import os
from datetime import date
import datetime
import sched, time
import json as simplejson
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from .models import Logwork, Furnace, Furnacework, Setusertemp, Settings, Powersettings, Dayandnight
from chartit import DataPool, Chart
from django.shortcuts import render_to_response


def f(x):
    return {
        'a': 1,
        'b': 2,
    }[x]
    
def days_hours_minutes(td):
    val = td.seconds//3600 *60 + (td.seconds*10//60)%60
    return val
    
def savetemperature(request):

    usertem = usertemp(request).content
    inroo = inroom(request).content
    if float(usertemp(request).content) == 0:
        usertem = float(0.01)
    else:
        usertem = usertemp(request).content
    val = (float(inroo) / float(usertem))*100
    furnaceisworking = Furnace.objects.order_by('-pub_date')[:1]
    furnaceworktemps = Furnacework.objects.order_by('-pub_date')[:1]
    furnacework = Furnacework.objects.all().order_by('-pub_date')
    
    furnaceworktemp = Furnacework.objects.order_by('-pub_date')[:1]
    workvaluepercent = workpercent(request).content

    power = Settings.objects.order_by('-pub_date')[:1]
    
    #print power[0].savefurnacepower
    #print power[0].saveweatherpower
    
    up = float(power[0].savefurnacepower) * float(workvaluepercent)/100
    down = float(power[0].saveweatherpower)
    temperatura = up - down
    #print temperatura
    lastnow = float(furnaceworktemp[0].temp) + temperatura
    
    
    if float(furnaceworktemps[0].temp) >= -20:
        q = Furnacework(temp=lastnow, pub_date=timezone.now(), tempstatus="-")
        q.save()
    else:
        q = Furnacework(temp=-20, pub_date=timezone.now(), tempstatus="-")
        q.save()

#ToDo
#settings for
#   up 
#   down
#

def savesettings(request):
    savefurnacepower = request.GET['savefurnacepower']
    saveweatherpower = request.GET['saveweatherpower']
    data = {savefurnacepower, saveweatherpower}
    s = Settings(saveweatherpower=saveweatherpower , savefurnacepower=savefurnacepower, pub_date=timezone.now())
    s.save()
    return HttpResponse(data)

def saveusertemp(request):
    usertemp = request.GET['usertemp']
    usertempnight = request.GET['usertempnight']
    data = {usertemp, usertempnight}
    #print usertemp
    s = Setusertemp(usertemp=usertemp, usertempnight=usertempnight, pub_date=timezone.now())
    s.save()
    return HttpResponse(data)

def savepowersettings(request):

    first = request.GET['first']
    second = request.GET['second']
    third = request.GET['third']
    fourth = request.GET['fourth']
    fifth = request.GET['fifth']
    data = {first, second, third, fourth, fifth}
    #print usertemp
    s = Powersettings(first=first, second=second, third=third, fourth=fourth, fifth=fifth , pub_date=timezone.now())
    s.save()
    return HttpResponse(data)

def settings(request):
    usertemp = Setusertemp.objects.order_by('-pub_date')[:1]
    settings = Settings.objects.order_by('-pub_date')[:1]
    powersettings = Powersettings.objects.order_by('-pub_date')[:1]
    context = { 'settings': settings, 'usertemp':usertemp, 'powersettings':powersettings }
    return render(request, 'driver/settings.html', context )


def index(request):
    furnace = Furnace.objects.values('work').order_by('-pub_date')[:1]
    context = { 'furnace': furnace}
    return render(request, 'driver/index.html', context )


def getdaynight(request):

    tmp = Dayandnight.objects.order_by('-pub_date')[:1]
    return HttpResponse(tmp[0].timeofday)
        
        
def dayornight(request):
    JSONdata = request.GET['status']
    dictt = simplejson.JSONDecoder().decode( JSONdata )
    if dictt == True:
        f = Dayandnight(timeofday="day", count="1", pub_date=timezone.now())
        f.save()
        return HttpResponse(dictt)
    else:
        f = Dayandnight(timeofday="night", count="1", pub_date=timezone.now())
        f.save()
        return HttpResponse(dictt)

def furnacework(request):
    JSONdata = request.GET['status']
    dictt = simplejson.JSONDecoder().decode( JSONdata )
    if dictt == True:
        f = Furnace(work=dictt, pub_date=timezone.now())
        f.save()
        return HttpResponse(dictt)
    else:
        f = Furnace(work=dictt, pub_date=timezone.now())
        f.save()
        return HttpResponse(dictt)


def blip(request):
    home = expanduser("~")
    sound = home +"/test.mp3"
    os.system("mplayer " + sound)
    return HttpResponseRedirect(reverse('driver:index'))
    
def sensors(request):
    savetemperature(request)
    import subprocess
    proc = subprocess.Popen('sensors', stdout=subprocess.PIPE)
    tmp = proc.stdout.read()

    return HttpResponse(tmp)
    
def inroom(request):

    tmp = Furnacework.objects.order_by('-pub_date')[:1]
    return HttpResponse(tmp[0].temp)
   
def onfurnace(request):
    usertemp = Setusertemp.objects.order_by('-pub_date')[:1]
    return HttpResponse(usertemp)
    
def usertemp(request):
    usertemp = Setusertemp.objects.order_by('-pub_date')[:1]
    #print usertemp[0].usertempnight
    dayornight = Dayandnight.objects.order_by('-pub_date')[:1]
    if dayornight[0].timeofday == "day":
        usertempdon = usertemp[0].usertemp
    else:
        usertempdon = usertemp[0].usertempnight
    return HttpResponse(usertempdon)
    
def workpercent(request):
    powersettings = Powersettings.objects.order_by('-pub_date')[:1]
    furnaceisworking = Furnace.objects.order_by('-pub_date')[:1]
    #print usertemp(request).content.usertempnight
    if float(usertemp(request).content) == 0:
        usertem = float(0.01)
    else:
        usertem = usertemp(request).content
    inroo = inroom(request).content
    if furnaceisworking[0].work == True:
        val = (float(inroo) / float(usertem))* 100
        if val <= 65 or furnaceisworking[0].work == False:
            work = 100
        elif (val > 65 and val <= 75) :
            work = powersettings[0].first
        elif (val > 75 and val <= 85) :
            work = powersettings[0].second
        elif (val > 85 and val <= 95) :
            work = powersettings[0].third
        elif (val > 95 and val <= 98) :
            work = powersettings[0].fourth
        elif (val > 98 and val <= 102) :
            work = powersettings[0].fifth
        else:
            work = 0

            
    else:
        work = 0
        
    return HttpResponse(work)


def weather_chart_view(request):
    weatherdata = \
        DataPool(
           series=
            [{'options': {
               'source': Furnacework.objects.all().order_by('-pub_date')[:100]},
              'terms': [ ('pub_date'),
                  'temp']}
             ])

    cht = Chart(
            datasource = weatherdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'pub_date': [
                    'temp']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Temperature data in room'},
               'xAxis': {
               'type': 'datetime',
               'dateTimeLabelFormats': {
                        'day': '%b %e'
                    },
                    'title': {
                       'text': 'Date'}},
               'yAxis': {
                    'title': {
                       'text': 'Temperature'}}
                       })

    context = { 'weatherchart': cht}
    return render(request, 'driver/test.html', context )
    
