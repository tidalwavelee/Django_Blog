from django import forms
from comment.models import Comment

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ("body","content_type","object_id")
    widgets = {
        "body": forms.Textarea(attrs={'cols': 60, 'rows': 6, 'placeholder': "请评论"}),
        "content_type": forms.HiddenInput(),
        "object_id": forms.HiddenInput(),
      }
