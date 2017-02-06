from django.conf.urls import url

from . import views

app_name = 'testdriver'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    
]
