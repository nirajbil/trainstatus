from django.contrib.auth.models import User
from django import forms
from .models import RecentPNR

"""
class PnrForms(forms.ModelForm):
    pnr_number = forms.CharField(max_length=6)

    class Meta:
         fields = ['pnr_number']

"""

"""
class RecentPnrForm(forms.ModelForm):
    class Meta:
        model = RecentPNR
        fields = ['RecentPnrNo']

"""