from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from userprofile.models import Profile
import datetime

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar','title','website','bio')
