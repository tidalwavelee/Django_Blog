from django import forms
from django.contrib.auth.models import User
from article.models import UserProfile
from article.models import Category,Article,UserProfile
from mdeditor.fields import MDTextFormField
import datetime

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name")
    article_number = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = Category
        fields = ('name',)

class ArticleForm(forms.ModelForm):
#    title = forms.CharField(max_length=128, help_text="Title")
#    body = MDTextFormField()
#    created_at = forms.DateTimeField(initial=datetime.date.today)

    class Meta:
        model = Article
        exclude = ('updated_at','read',)

#class UserForm(forms.ModelForm):
#    password = forms.CharField(widget=forms.PasswordInput())
#
#    class Meta:
#        model = User
#        fields=('username','email','password')
#
#class UserProfileForm(forms.ModelForm):
#    class Meta:
#        model = UserProfile
#        fields = ('title','website','picture')
