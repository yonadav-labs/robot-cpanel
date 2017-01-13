from django.contrib import admin
from .models import *

class ScheduleTablularInline(admin.TabularInline):
    model = Schedule
    extra = 0
    fields = ['dow', 'start_time', 'end_time']


class DeviceAdmin(admin.ModelAdmin):
    inlines = [ScheduleTablularInline]
    class Meta:
        model = Device

admin.site.register(Device, DeviceAdmin)
admin.site.register(UserProfile)
admin.site.register(Firmware)
