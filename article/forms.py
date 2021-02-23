from django import forms
from django.utils.translation import gettext_lazy as _
from article.models import Category,Article
from mdeditor.fields import MDTextFormField
import datetime

class CategoryForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
      model = Category
      fields = ('emblem','name','bio','article_content',)
      labels = {
          "emblem": _("版徽"),
          "name": _("版面名"),
          "bio": _("简介"),
          "article_content": _("文章目录"),
        }

class ArticleForm(forms.ModelForm):
  class Meta:
    model = Article
    fields = ('title','category','body',)
    labels = {
        "title": _("文章标题"),
        "category": _("文章分类"),
        "body": _("文章正文"),
      }
