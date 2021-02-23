from django import forms
from django.utils.translation import gettext_lazy as _
from guide.models import Question, Answer
from mdeditor.fields import MDTextFormField


class QuestionForm(forms.ModelForm):
  status = forms.CharField(widget=forms.HiddenInput())
  class Meta:
    model = Question
    fields = ("title", "content", "tags", "status",)
    labels = {
        "title": _("标题"),
        "tags": _("标签"),
        "content": _("正文"),
        "status": _("状态"),
      }
