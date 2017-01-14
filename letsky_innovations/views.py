import os, sys
import mimetypes

from wsgiref.util import FileWrapper

from django.utils.encoding import smart_str
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

from device.models import *

def home(request):
    return render(request, 'home.html')


def download_firmware(request):
	firmware = Firmware.objects.filter(active=True).order_by('-updated_at').first()
	if firmware:	
		filename = settings.BASE_DIR+firmware.source.url
		return get_download_response(filename)


def get_download_response(path):
    wrapper = FileWrapper( open( path, "r" ) )
    content_type = mimetypes.guess_type( path )[0]

    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize( path ) # not FileField instance
    response['Content-Disposition'] = 'attachment; filename=%s/' % smart_str( os.path.basename( path ) )
    return response
