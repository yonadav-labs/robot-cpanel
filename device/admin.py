from django.contrib import admin
from .models import *

class ScheduleTablularInline(admin.TabularInline):
    model = Schedule
    extra = 0
    fields = ['dow', 'start_time', 'end_time']


class GPSTablularInline(admin.TabularInline):
    model = GPSInfo
    extra = 0
    fields = ['geo_type', 'geo_points']


class DeviceAdmin(admin.ModelAdmin):
    inlines = [ScheduleTablularInline, GPSTablularInline]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_superuser:
            self.exclude = ()
        else:
            self.exclude = ('user',)

        return super(DeviceAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        if request.user.is_superuser:
            self.exclude = ()
        else:
            self.exclude = ('user',)
            
        return super(DeviceAdmin, self).add_view(request, 
            form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(DeviceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    class Meta:
        model = Device


admin.site.register(Device, DeviceAdmin)
admin.site.register(UserProfile)
admin.site.register(Firmware)
