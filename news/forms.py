from django import forms
from django.utils.translation import gettext_lazy as _
from news.models import News

class NewsForm(forms.ModelForm):
  class Meta:
      model = News
      fields = ('title','category','body',)
      labels = {
          "title": _("文章标题"),
          "category": _("文章分类"),
          "body": _("文章正文"),
        }
