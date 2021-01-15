from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from mdeditor.fields import MDTextField
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    article_number = models.IntegerField(default=0)
    emblem = models.ImageField(upload_to='category/%Y%m%d/', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.replace('.','_'))
        category = super(Category, self).save(*args, **kwargs)
       # 固定宽度缩放图片大小
        if self.emblem and not kwargs.get('update_fields'):
          image = Image.open(self.emblem)
          (x, y) = image.size
          new_x = 260
          new_y = int(new_x * (y / x))
          resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
          resized_image.save(self.emblem.path)
        return category


    def __str__(self):
        return self.name

class ReadNum(models.Model):
  number = models.PositiveIntegerField(default=0)
  content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey('content_type','object_id')

  def __str__(self):
    return f"ReadNum:{self.content_type}:{self.object_id}:{self.number}"

class LikeNum(models.Model):
  number = models.PositiveIntegerField(default=0)
  content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey('content_type','object_id')

  def __str__(self):
    return f"LikeNum:{self.content_type}:{self.object_id}:{self.number}"

class Article(models.Model):
  category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
  title = models.CharField(max_length=64)
  body = MDTextField()
  author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  read_num = GenericRelation(ReadNum)
  like_num = GenericRelation(LikeNum)

  def save(self, *args, **kwargs):
    super(Article, self).save(*args, **kwargs)

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

