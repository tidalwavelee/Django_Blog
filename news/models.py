from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from mdeditor.fields import MDTextField
from article.models import Category,ReadNum,LikeNum

class News(models.Model):
  category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
  title = models.CharField(max_length=64)
  body = MDTextField()
  author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  read_num = GenericRelation(ReadNum)
  like_num = GenericRelation(LikeNum)

  def save(self, *args, **kwargs):
    super(News, self).save(*args, **kwargs)

  def read(self):
    if self.read_num.first():
      return self.read_num.first().number
    else:
      return 0
  def likes(self):
    if self.like_num.first():
      return self.like_num.first().number
    else:
      return 0

  def __str__(self):
    return self.title
  class Meta:
    ordering = ['-created_at']

