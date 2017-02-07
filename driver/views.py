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
    val = (float(inroo) / float(usertem))*100
    furnaceisworking = Furnace.objects.order_by('-pub_date')[:1]
    #print furnaceisworking[0].work
    furnaceworktemps = Furnacework.objects.order_by('-pub_date')[:1]
    furnacework = Furnacework.objects.all().order_by('-pub_date')
    
    furnaceworktemp = Furnacework.objects.order_by('-pub_date')[:1]
    workvaluepercent = workpercent(request).content
    #print workvaluepercent
    statusofwork =  Furnacework.objects.all().order_by('-pub_date')[:6]
    if furnaceisworking[0].work == True:
        if statusofwork[3].tempstatus == "down" :
            print statusofwork[5].tempstatus + " :O" 
            tempi = 100
            downn = False
        elif statusofwork[1].tempstatus == "down" :
            print statusofwork[1].tempstatus + " :O" 
            tempi = 125
            downn = True
        elif statusofwork[2].tempstatus == "down" :
            print statusofwork[2].tempstatus + " :O" 
            tempi = 125
            downn = True
       #elif statusofwork[3].tempstatus == "down" :
       #     print statusofwork[3].tempstatus + " :O" 
       #     tempi = 125
       #     downn = True
        #elif statusofwork[4].tempstatus == "down" :
       #     print statusofwork[4].tempstatus + " :O" 
        #    tempi = 125
        #    downn = True
        elif statusofwork[0].tempstatus == "down":
            downn = False
            
            tempi = 100
            print statusofwork[4].tempstatus + " 5 is up"
            
            
        #if (int(workvaluepercent) <= int(80)):
            #tempi = 3
       # elif (int(workvaluepercent) <= int(96)) and (int(workvaluepercent) > int(80)):
            #tempi = 1.025
       # elif (int(workvaluepercent) <= int(98)) and (int(workvaluepercent) > int(96)):
           # tempi = 1.02

       # elif (int(workvaluepercent) > int(98)) and (int(workvaluepercent) <= int(102)) :
            #tempi = 1.025
       # else:
        #    tempi = 1
    else:
        tempi = 100

 
    
    print downn
    #print workvaluepercent
    up = 0.27 * float(workvaluepercent)/100
    down = float(0.2)*float(tempi)/100
    print "down " + str(up)
    temperatura = up - down
    print temperatura
    lastnow = float(furnaceworktemp[0].temp) + temperatura
    if temperatura <= 0 or downn == False:
        status = "down"
    else:
        status = "up"
    #print status
    if float(furnaceworktemps[0].temp) >= 0:
        q = Furnacework(temp=lastnow, pub_date=timezone.now(), tempstatus=status)
        q.save()
    else:
        q = Furnacework(temp=0, pub_date=timezone.now(), tempstatus="up")
        q.save()
    
    






    

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
    #p = Logwork(data=tmp, pub_date=timezone.now())
    #p.save()
    #tmp = ""
    return HttpResponse(tmp)
    
def inroom(request):

    tmp = Furnacework.objects.order_by('-pub_date')[:1]
#    inroomtemp = tmp[0].temp
#    stringtemp = str(inroomtemp)
#    print len(str(stringtemp))-1
    return HttpResponse(tmp[0].temp)
   
def onfurnace(request):
    usertemp = Setusertemp.objects.order_by('-pub_date')[:1]
    #tmp = 54
    return HttpResponse(usertemp)
    
def usertemp(request):
    usertemp = Setusertemp.objects.order_by('-pub_date')[:1]
    #tmp = 54
    return HttpResponse(usertemp)
    
def workpercent(request):
    furnaceisworking = Furnace.objects.order_by('-pub_date')[:1]
    usertem = usertemp(request).content
    inroo = inroom(request).content
    val = (float(inroo) / float(usertem))*100
    if furnaceisworking[0].work == True:
        if (float(inroo) / float(usertem))* 100 <= 85 or furnaceisworking[0].work == False:
            temp = 100
        elif ((float(inroo) / float(usertem))*100 <= 94) and ((float(inroo) / float(usertem))*100 > 85):
            temp = 90
        elif ((float(inroo) / float(usertem))*100 <= 96 and (float(inroo) / float(usertem))*100 > 94) :
            temp = 88
        elif ((float(inroo) / float(usertem))*100 <= 98) and ((float(inroo) / float(usertem))*100 > 96):
            temp = 82
        elif ((float(inroo) / float(usertem))*100 <= 100) and ((float(inroo) / float(usertem))*100 > 98):
            temp = 75
        elif ((float(inroo) / float(usertem))*100 > 100 and (float(inroo) / float(usertem))*100 <= 102) :
            temp = 65
        else:
            temp = 0
    else:
        temp = 0
        
    return HttpResponse(temp)




def weather_chart_view(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
           series=
            [{'options': {
               'source': Furnacework.objects.all().order_by('-pub_date')[:100]},
              'terms': [ 'pub_date',
                  'temp']}
             ])

    #Step 2: Create the Chart object
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
                   'text': 'Weather Data of Boston and Houston'},
               'xAxis': {
                    'title': {
                       'text': 'Month number'}}})

    #Step 3: Send the chart object to the template.
   # return render_to_response({'weatherchart': cht})
    context = { 'weatherchart': cht}
    return render(request, 'driver/test.html', context )
    
    #return render_to_response('driver/test.html', {'weatherchart': cht})
