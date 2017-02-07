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
from .models import Logwork, Furnace, Furnacework, Setusertemp
from chartit import DataPool, Chart
from django.shortcuts import render_to_response



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
    
    up = 1.27 * float(workvaluepercent)/100
    down = float(1)
    temperatura = up - down
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

def savefurnacepower(request):
    furnace = Furnace.objects.values('work').order_by('-pub_date')[:1]
    context = { 'furnace': furnace}
    return render(request, 'driver/settings.html', context )

def saveweatherpower(request):
    if request.method == 'POST':
        do_something_else()
    return render(request, 'driver/settings.html', context ) 

def settings(request):
    furnace = Furnace.objects.values('work').order_by('-pub_date')[:1]
    context = { 'furnace': furnace}
    return render(request, 'driver/settings.html', context )


def index(request):
    furnace = Furnace.objects.values('work').order_by('-pub_date')[:1]
    context = { 'furnace': furnace}
    return render(request, 'driver/index.html', context )



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
    return HttpResponse(usertemp)
    
def workpercent(request):
    furnaceisworking = Furnace.objects.order_by('-pub_date')[:1]
    if float(usertemp(request).content) == 0:
        usertem = float(0.01)
    else:
        usertem = usertemp(request).content
    inroo = inroom(request).content
    val = (float(inroo) / float(usertem))*100
    if furnaceisworking[0].work == True:
        if (float(inroo) / float(usertem))* 100 <= 85 or furnaceisworking[0].work == False:
            work = 100
        elif ((float(inroo) / float(usertem))*100 <= 94) and ((float(inroo) / float(usertem))*100 > 85):
            work = 90
        elif ((float(inroo) / float(usertem))*100 <= 96 and (float(inroo) / float(usertem))*100 > 94) :
            work = 88
        elif ((float(inroo) / float(usertem))*100 <= 100) and ((float(inroo) / float(usertem))*100 > 96):
            work = 82
        elif ((float(inroo) / float(usertem))*100 > 100 and (float(inroo) / float(usertem))*100 <= 102) :
            work = 65
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
              'terms': [ 'pub_date',
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
                    'title': {
                       'text': 'Date'}},
               'yAxis': {
                    'title': {
                       'text': 'Temperature'}}
                       })

    context = { 'weatherchart': cht}
    return render(request, 'driver/test.html', context )
    
