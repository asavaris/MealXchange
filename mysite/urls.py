	
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^(?i)Xchange/', include('polls.urls')),
    url(r'^(?i)admin/', include(admin.site.urls)),
    url(r'^(?i)accounts/', include('registration.backends.default.urls')),
]

