from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    website = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='profile_images/%Y%m%d/',blank=True)
    title = models.CharField(max_length=64,blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
      return f"<profile:{self.user.username}>"
