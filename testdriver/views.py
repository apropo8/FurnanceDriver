from django.shortcuts import render

def index(request):
    #furnace = Furnace.objects.values('work').order_by('-pub_date')[:1]
    context = { 'furnace': "dd"}
    return render(request, 'testdriver/index.html', context )
