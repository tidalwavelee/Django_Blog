from django import forms
from django.contrib.auth.models import User
from article.models import UserProfile
from article.models import Category,Article,UserProfile
import datetime

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name")
    article_number = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = Category
        fields = ('name',)

class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Title")
    article = forms.CharField(widget=forms.Textarea, help_text="Content")
    publish_date = forms.DateField(initial=datetime.date.today)
    read = forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    class Meta:
        model = Article
        exclude = ('last_updated_time',)

#    def clean(self):
#        cleaned_data = self.cleaned_data
#        read = cleaned_data.get('read')
#        if not read:
#            cleaned_data['read'] = 0
#        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields=('username','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('title','website','picture')
