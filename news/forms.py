from django import forms
from django.utils.translation import gettext_lazy as _
from news.models import News

class NewsForm(forms.ModelForm):
  class Meta:
      model = News
      fields = ('title','category','body',)
      labels = {
          "title": _("标题"),
          "category": _("分类"),
          "body": _("正文"),
        }
