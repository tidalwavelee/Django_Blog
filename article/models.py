from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from mdeditor.fields import MDTextField

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    article_number = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.replace('.','_'))
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class ReadNum(models.Model):
  number = models.IntegerField(default=0)
  content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey('content_type','object_id')

  def __str__(self):
    return f"ReadNum:{self.content_type}:{self.object_id}:{self.number}"

class Article(models.Model):
  category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
  title = models.CharField(max_length=64)
  body = MDTextField()
  author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  read_num = GenericRelation(ReadNum)

  def save(self, *args, **kwargs):
    super(Article, self).save(*args, **kwargs)
  def read(self):
    if self.read_num.first():
      return self.read_num.first().number
    else:
      return 0
  def __str__(self):
    return self.title
  class Meta:
    ordering = ['-created_at']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images',blank=True)
    title = models.CharField(max_length=64,blank=True)

    def __str__(self):
        return self.user.username
