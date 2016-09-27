from django.contrib import admin

from .models import PNRNotification, PNRStatus

admin.site.register(PNRNotification)
admin.site.register(PNRStatus)
