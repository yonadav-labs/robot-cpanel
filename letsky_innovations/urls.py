from django.conf.urls import url, include
from django.contrib import admin

from views import *

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name="home"),
    url(r'^download_firmware', download_firmware, name="download_firmware")
]
