from collections import Counter
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from mdeditor.fields import MDTextField
import markdown
from comment.models import Vote
from region.models import Region

class EventQuerySet(models.query.QuerySet):
  def get_event(self,in_code):
    return self.filter(area_code__startswith=area_code)
  def get_counted_tags(self):
    tag_dict = {}
    query = self.all().annotate(tagged=Count("tags")).filter(tags__gt=0)
    for obj in query:
      for tag in obj.tags.names():
        if tag not in tag_dict:
          tag_dict[tag] = 1
        else:
          tag_dict[tag] += 1
    return tag_dict.items()

class Event(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=200, unique=True, blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  content = MDTextField()
  total_votes = models.IntegerField(default=0)
  votes = GenericRelation(Vote)
  tags = TaggableManager()
  area = models.ForeignKey(Region, on_delete=models.CASCADE)
  objects = EventQuerySet.as_manager()

  class Meta:
    ordering = ["-created_at"]
    verbose_name = _("Event")
    verbose_name_plural = _("Events")

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
  def __str__(self):
    return self.title

  def get_markdown(self):
    md = markdown.Markdown(
           extensions=['markdown.extensions.extra',
                       'markdown.extensions.codehilite',
                       'markdown.extensions.toc']
         )
    return md.convert(self.content)

  def count_votes(self):
    """Method to update the sum of the total votes. Uses this complex query
    to avoid race conditions at database level."""
    dic = Counter(self.votes.values_list("value", flat=True))
    Event.objects.filter(id=self.id).update(total_votes=dic[True] - dic[False])
    self.refresh_from_db()

  def get_upvoters(self):
    return [vote.user for vote in self.votes.filter(value=True)]
  def get_downvoters(self):
    return [vote.user for vote in self.votes.filter(value=False)]
