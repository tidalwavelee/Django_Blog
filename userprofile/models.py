from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  website = models.URLField(blank=True)
  avatar = models.ImageField(upload_to='profile_images/%Y%m%d/',blank=True)
  title = models.CharField(max_length=64,blank=True)
  bio = models.TextField(max_length=500, blank=True)

  def __str__(self):
    return f"<profile:{self.user.username}>"

  def get_following(self):
    '''关注的人'''
    user_list = []
    for followed_user in self.user.following.all():
      user_list.append(followed_user.followed)
    return user_list

  def get_followed(self):
    '''粉丝'''
    user_list = []
    for following_user in self.user.followed.all():
      user_list.append(following_user.following)
    return user_list

class FollowRelation(models.Model):
  followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
  following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return f"followed:{self.followed},following:{self.following}"

class Favorite(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()

  class Meta:
    ordering = ["-created_at"]
