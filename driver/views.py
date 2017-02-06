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


def days_hours_minutes(td):
    val = td.seconds//3600 *60 + (td.seconds*10//60)%60
    return val
    
def savetemperature(request):

    usertem = usertemp(request).content
    inroo = inroom(request).content
    val = (float(inroo) / float(usertem))*100
    furnaceisworking = Furnace.objects.order_by('-pub_date')[:1]
    print furnaceisworking[0].work
    furnaceworktemps = Furnacework.objects.order_by('-pub_date')[:1]
    furnacework = Furnacework.objects.all().order_by('-pub_date')
    
    furnaceworktemp = Furnacework.objects.order_by('-pub_date')[:1]
    workvaluepercent = workpercent(request).content
    
    #print workvaluepercent
    up = 1.23 * float(workvaluepercent)/100
    down = float(1)
    temperatura = up - down
    lastnow = float(furnaceworktemp[0].temp) + temperatura
    print up
    if float(furnaceworktemps[0].temp) >= 0:
        q = Furnacework(temp=lastnow, pub_date=timezone.now(), tempstatus="up")
        q.save()
    else:
        q = Furnacework(temp=0, pub_date=timezone.now(), tempstatus="up")
        q.save()
    
    
    
    #if float(furnaceworktemps[0].temp) >= 0:
    #    if ((float(inroo) / float(usertem))* 100 >= 100 and  (float(inroo) / float(usertem))* 100 >= 100 ) or furnaceisworking[0].work == False: #and (float(inroo) / float(usertem))* 100 <= 101:
#
#            furnaceworktemp = Furnacework.objects.order_by('-pub_date')[:1]
#
#            tempdown = float(furnaceworktemp[0].temp) - 0.1# - (float(days_hours_minutes(delta2))+0.1)
#           
#            print "down"
#            q = Furnacework(temp=tempdown, pub_date=timezone.now(), tempstatus="down")
#            q.save()
#        elif ((float(inroo) / float(usertem))* 100 <= 100 ) or furnaceisworking[0].work == True:
#            
#            furnaceworktemp = Furnacework.objects.order_by('-pub_date')[:2]
#           
#            tempup = float(furnaceworktemp[0].temp) + 0.1# + (float(days_hours_minutes(delta2))+0.1)
#         
#            print "up"
#            q = Furnacework(temp=tempup, pub_date=timezone.now(), tempstatus="up")
#            q.save()
#    else:
#        q = Furnacework(temp=0, pub_date=timezone.now(), tempstatus="up")
#        q.save()
        






    

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
        elif ((float(inroo) / float(usertem))*100 <= 96) and ((float(inroo) / float(usertem))*100 > 85):
            temp = 100
        elif ((float(inroo) / float(usertem))*100 <= 98) and ((float(inroo) / float(usertem))*100 > 96):
            temp = 90

        elif ((float(inroo) / float(usertem))*100 > 98 and (float(inroo) / float(usertem))*100 <= 102) :
            temp = 85
        else:
            temp = 0
    else:
        temp = 0
        
    return HttpResponse(temp)


