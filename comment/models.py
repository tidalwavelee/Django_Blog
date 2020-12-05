from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
  created_at = models.DateTimeField(auto_now_add=True)
  body = models.TextField()

  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()

  class Meta:
    ordering = ["-created_at"]
