from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    article_number = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.replace('.','_'))
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=128)
    article = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    read = models.IntegerField(default=0)
    slug = models.SlugField(unique=True,max_length=128)

    def get_unique_slug(self):
        title_slug = slugify(self.title.replace(' ','_'))
        date_slug = slugify(self.publish_date)
        unique_slug = title_slug+'_'+date_slug
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images',blank=True)
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.user.username
