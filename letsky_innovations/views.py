import json
import os, sys
import mimetypes
from datetime import datetime
from wsgiref.util import FileWrapper

from django.utils.encoding import smart_str
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from device.models import *

def home(request):
    geo_info = {"permitted": [],
                "excluded": [],
                "trace": []}

    if request.user.is_authenticated():
        for device in Device.objects.filter(user=request.user):
            for p_info in GPSInfo.objects.filter(device=device):
                item = p_info.geo_points.split('@')

                geo_info[p_info.geo_type].append({"data":[map(float, ii.split(',')) for ii in item], 
                                                  "name": device.name,
                                                  "img": device.img.url})

    return render(request, 'home.html', {'geo_info': geo_info})


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


def get_schedule(request, device_id):
    device = Device.objects.filter(device_id=device_id).first()
    if device:
        schedule = Schedule.objects.filter(device=device)
        schedule = ["{}, {}, {}".format(item.dow, item.start_time.strftime('%H%M'), item.end_time.strftime('%H%M')) for item in schedule]
        return HttpResponse('@'.join(schedule))
    return HttpResponse('')


def get_pattern(request, device_id):
    device = Device.objects.filter(device_id=device_id).first()
    if device:
        return HttpResponse(device.pattern)
    return HttpResponse('')


@csrf_exempt
def send_geoinfo(request, device_id):
    """
    {
        type: "permitted" / "excluded" / "trace",
        gps: "51.3265,-1.2356@51.3265,-1.2356@51.3265,-1.2356@51.3265,-1.2356",
    }
    """
    if request.method == "POST":
        type_ = json.loads(request.body).get('type')
        gps = json.loads(request.body).get('gps')
        try:
            device = Device.objects.get(device_id=device_id)
            if type_ == "trace":
                gps = gps.split('@')[-1]
                gps_trace, created = GPSInfo.objects.get_or_create(device=device, 
                                                                   geo_type=type_, 
                                                                   defaults={'geo_points': gps})
                if not created:
                    gps_trace.geo_points = gps_trace.geo_points + "@" + gps
                    gps_trace.save()
            else:
                GPSInfo.objects.create(device=device, geo_type=type_, geo_points=gps)
            return HttpResponse('success')
        except Exception, e:
            pass
    return HttpResponse('fail')
