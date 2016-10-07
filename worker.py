import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railway.settings")
from django.conf import settings
django.setup()

from userpanal.tasks import *
from userpanal.models import *
from datetime import timedelta, datetime
import time

TIME_CONST = 1


"""
pnr_notifications = PNRNotification.objects.all()
for pnr_notification in pnr_notifications:
    print "pnr_notification=%s " %pnr_notification
    print pnr_notification.pnr_no
    print pnr_notification.notification_type
    print pnr_notification.notification_type_value
    print pnr_notification.notification_frequency
    print pnr_notification.notification_frequency_value
    print pnr_notification.next_schedule_time

findtime = datetime.now()+timedelta(minutes=1)
pnr_notifications.object.next_schedule_time == findtime
"""

while True:
    try:
        #print 'I am doing something'
        pnr_notifications = PNRNotification.objects.filter(next_schedule_time__lte=(datetime.now()+timedelta(minutes=TIME_CONST)))

        begin = time.time()
        print "begin=%s " %begin

        for pnr_notification in pnr_notifications:
            print "next_schedule_time=%s " %pnr_notification.next_schedule_time
            print "pnr_notification=%s " %pnr_notification.notification_frequency_value
            print "datetime.now()=%s, timedelta=%s" %(datetime.now(),timedelta(minutes=TIME_CONST))
            print "pnr_notification timedelta =%s " %(datetime.now()+timedelta(minutes=TIME_CONST))
            schedule_pnr_notification(pnr_notification)
        end = time.time()
        print "end=%s " %end

        diff = int(end-begin)
        print "diff=%s" %diff

        sleep_time = int((TIME_CONST*60) - (diff/60))
        print 'sleeping for %s min' % (sleep_time/60)
        if sleep_time>0:
            time.sleep(sleep_time)
    except:
        # Send email/sms notification to me.
        #print 'I am doing something Error......'
        pass



