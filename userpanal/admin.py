from django.contrib import admin

from .models import PNRNotification, PNRStatus, RecentPNR, API_Key
from userpanal.models import UserProfile

admin.site.register(PNRNotification)
admin.site.register(PNRStatus)
admin.site.register(UserProfile)
admin.site.register(API_Key)


admin.site.register(RecentPNR)