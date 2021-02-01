from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from userprofile.models import Profile, Favorite
import datetime

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ('avatar','title','website','bio')

class FavoriteForm(forms.ModelForm):
  class Meta:
    model = Favorite
    fields = ("content_type","object_id")
