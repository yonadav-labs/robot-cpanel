from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="info")
    address = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

PATTERN = (
        (0, 'N-S'),
        (0, 'E-W')
    )

class Device(models.Model):
    user = models.ForeignKey(User)
    device_id = models.CharField('Device ID', max_length=30, unique=True)
    name = models.CharField(max_length=100)    
    img = models.FileField(upload_to='devices', 
        default="devices/default.png")
    pattern = models.IntegerField(choices=PATTERN, default=0)
    download_firmware = models.BooleanField(default=False)

    def __unicode__(self):
        return "{} ({})".format(self.device_id, self.name)

DOW = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

class Schedule(models.Model):
    device = models.ForeignKey(Device)
    dow = models.IntegerField('Day of Week', choices=DOW)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Firmware(models.Model):
    version = models.CharField(max_length=10, default="1.0")
    # title = models.CharField(max_length=100, null=True, blank=True)
    source = models.FileField(upload_to='firmware')
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.version


class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form):
        user.is_staff = True
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        return super(MyAccountAdapter, self).save_user(request, user, form)
