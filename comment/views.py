from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from comment.forms import CommentForm
# from comment.models import Comment

@login_required
def add_comment(request):
  referer = request.META.get('HTTP_REFERER', reverse('article:index')) 
  if request.method == 'POST':
    text = request.POST.get('body','').strip()
    if text.isspace():
      return redirect(referer)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
      comment = comment_form.save(commit=False)
      comment.user = request.user
      comment.save()
  else:
    comment_form = CommentForm()
  return redirect(referer)

  
