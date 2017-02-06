from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^driver/', include('driver.urls')),
    url(r'^test/', include('testdriver.urls')),
    url(r'^admin/', admin.site.urls),
]
