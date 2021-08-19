import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  body = models.TextField()

  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()

  class Meta:
    ordering = ["-created_at"]

class Vote(models.Model):
  uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  value = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  content_type = models.ForeignKey(ContentType, related_name="votes_on", on_delete=models.CASCADE)
  object_id = models.CharField(max_length=50, blank=True, null=True)
  vote = GenericForeignKey("content_type", "object_id")

  class Meta:
    verbose_name = _("Vote")
    verbose_name_plural = _("Votes")
    index_together = ("content_type", "object_id")
    unique_together = ("user", "content_type", "object_id")
