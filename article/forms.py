from django import forms
from django.utils.translation import gettext_lazy as _
from article.models import Category,Article
from mdeditor.fields import MDTextFormField
import datetime

class CategoryForm(forms.ModelForm):
    article_number = forms.IntegerField(widget=forms.HiddenInput(),initial=0,required=False)
    slug = forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = Category
        fields = ('emblem','name','bio',)

class ArticleForm(forms.ModelForm):
  class Meta:
      model = Article
      fields = ('title','category','body',)
      labels = {
          "title": _("文章标题"),
          "category": _("文章分类"),
          "body": _("文章正文"),
        }
