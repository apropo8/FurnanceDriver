import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class Logwork(models.Model):

    data = models.TextField()
    pub_date = models.DateTimeField('date published')
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
        
    def __str__(self):
        return self.data


#@python_2_unicode_compatible  # only if you need to support Python 2
class Furnace(models.Model):

    work = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
        

    def __unicode__(self):
        return unicode(self.work)
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
    
class Furnacework(models.Model):

    temp = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    tempstatus = models.CharField(max_length = 200)

    def __unicode__(self):
        return unicode(self.temp)    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
    
class Setusertemp(models.Model):

    usertemp = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    

    def __unicode__(self):
        return unicode(self.usertemp)    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
    
    
    
    
    
#@python_2_unicode_compatible  # only if you need to support Python 2
#class Choice(models.Model):

#    question = models.ForeignKey(Question, on_delete=models.CASCADE)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)
#    
#    def __str__(self):
#        return self.choice_text


