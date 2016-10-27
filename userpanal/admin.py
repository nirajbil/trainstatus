from django.contrib import admin

from .models import PNRNotification, PNRStatus, RecentPNR
from userpanal.models import UserProfile

admin.site.register(PNRNotification)
admin.site.register(PNRStatus)
admin.site.register(UserProfile)

admin.site.register(RecentPNR)