from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()

@register.simple_tag
def retrieve_comments(obj):
  obj_content_type = ContentType.objects.get_for_model(obj) 
  comments = Comment.objects.filter(content_type=obj_content_type, object_id=obj.pk)
  return comments

@register.simple_tag
def get_comment_form(obj):
  obj_content_type = ContentType.objects.get_for_model(obj) 
  comment_form = CommentForm(initial={'content_type': obj_content_type,'object_id': obj.pk})
  return comment_form
