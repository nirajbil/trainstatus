from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib


class PNRNotification(models.Model):
    pnr_no = models.CharField(max_length=20)
    notification_type = models.CharField(max_length=10)
    notification_type_value = models.CharField(max_length=50)
    notification_frequency = models.CharField(max_length=20)
    notification_frequency_value = models.CharField(max_length=10)
    next_schedule_time = models.DateTimeField()
    notify_on_status_change = models.BooleanField(default=False)


class PNRStatus(models.Model):
    pnr_no = models.CharField(max_length=20)
    status = JSONField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    about_me = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'

    def profile_image_url(self):
        """
        Return the URL for the user's Facebook icon if the user is logged in via Facebook,
        otherwise return the user's Gravatar URL
        """
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=40".format(
            hashlib.md5(self.user.email).hexdigest())

    def account_verified(self):
        """
        If the user is logged in and has verified hisser email address, return True,
        otherwise return False
        """
        result = EmailAddress.objects.filter(email=self.user.email)
        if len(result):
            return result[0].verified
        return False


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])