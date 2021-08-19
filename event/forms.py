from django import forms
from django.utils.translation import gettext_lazy as _
from event.models import Event

class EventForm(forms.ModelForm):
  class Meta:
    model = Event
    fields = ("title", "content", "tags", "area_code",)
    labels = {
        "title": _("标题"),
        "tags": _("标签"),
        "content": _("正文"),
        "area_code": _("区域"),
    }
