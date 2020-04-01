from django import forms
from blog.models import Category,Article
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
    slug = forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = Article
        exclude = ('last_updated_time',)
