from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.conf import settings

from allauth.account.adapter import DefaultAccountAdapter


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="info")
    address = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

PATTERN = (
        ('N-S', 'N-S'),
        ('E-W', 'E-W')
    )

class Device(models.Model):
    user = models.ForeignKey(User)
    device_id = models.CharField('Device ID', max_length=30, unique=True)
    name = models.CharField(max_length=100)    
    img = models.FileField(upload_to='devices', 
        default="devices/default.png")
    pattern = models.CharField(max_length=5, choices=PATTERN, default='N-S')
    download_firmware = models.BooleanField(default=False)

    def __unicode__(self):
        return "{} ({})".format(self.device_id, self.name)

DOW = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

class Schedule(models.Model):
    device = models.ForeignKey(Device)
    dow = models.CharField('Day of Week', max_length=20, choices=DOW)
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

TYPE = (
        ('permitted', 'permitted'),
        ('excluded', 'excluded'),
        ('trace', 'trace'),
    )

class GPSInfo(models.Model):
    device = models.ForeignKey(Device)
    geo_type = models.CharField(max_length=20, choices=TYPE)
    geo_points = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{}-{}".format(self.device.name, self.geo_type)


class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form):
        user.is_staff = True
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        user = super(MyAccountAdapter, self).save_user(request, user, form)
        # grant permission
        permission = Permission.objects.get(name='Can add device')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can delete device')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can change device')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can add schedule')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can delete schedule')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can change schedule')
        user.user_permissions.add(permission)

        UserProfile.objects.create(user=user, 
                                   address=request.POST.get('address'),
                                   phone=request.POST.get('phone'))

        return user
