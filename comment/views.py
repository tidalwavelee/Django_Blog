from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from comment.forms import CommentForm

@login_required
def add_comment(request):
  data={"status": "ERROR"}
  if request.is_ajax():
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
      comment = comment_form.save(commit=False)
      comment.user = request.user
      comment.save()
      data["status"] = 'SUCCESS'
      data["username"] = comment.user.username
      data["comment_time"] = comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
      data["comment_body"] = comment.body
    else:
      data["status"] = '无效数据'
  else:
    comment_form = CommentForm()
    data["status"] = 'Cannot used for query!'
  return JsonResponse(data)
  
