from django.contrib import admin
from .models import *

class ScheduleTablularInline(admin.TabularInline):
    model = Schedule
    extra = 0
    fields = ['dow', 'start_time', 'end_time']


class DeviceAdmin(admin.ModelAdmin):
    exclude = ('user',)
    inlines = [ScheduleTablularInline]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    class Meta:
        model = Device

admin.site.register(Device, DeviceAdmin)
admin.site.register(UserProfile)
admin.site.register(Firmware)
