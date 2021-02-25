import uuid
from collections import Counter
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from mdeditor.fields import MDTextField
import markdown

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

class QuestionQuerySet(models.query.QuerySet):
  def get_answered(self):
    return self.filter(has_answer=True)
  def get_unanswered(self):
    return self.filter(has_answer=False)
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

class Question(models.Model):
  OPEN = "O"
  CLOSED = "C"
  DRAFT = "D"
  STATUS = ((OPEN, _("Open")), (CLOSED, _("Closed")), (DRAFT, _("Draft")))
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=200, unique=True, blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
  content = MDTextField()
  has_answer = models.BooleanField(default=False)
  total_votes = models.IntegerField(default=0)
  votes = GenericRelation(Vote)
  tags = TaggableManager()
  objects = QuestionQuerySet.as_manager()

  class Meta:
    ordering = ["-created_at"]
    verbose_name = _("Question")
    verbose_name_plural = _("Questions")
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
  def __str__(self):
    return self.title

  @property
  def count_answers(self):
    return Answer.objects.filter(question=self).count()

  def count_votes(self):
    """Method to update the sum of the total votes. Uses this complex query
    to avoid race conditions at database level."""
    dic = Counter(self.votes.values_list("value", flat=True))
    Question.objects.filter(id=self.id).update(total_votes=dic[True] - dic[False])
    self.refresh_from_db()
  def get_upvoters(self):
    return [vote.user for vote in self.votes.filter(value=True)]
  def get_downvoters(self):
    return [vote.user for vote in self.votes.filter(value=False)]

  def get_answers(self):
    return Answer.objects.filter(question=self)
  def get_accepted_answer(self):
    return Answer.objects.get(question=self, is_answer=True)
  def get_markdown(self):
    md = markdown.Markdown(
           extensions=['markdown.extensions.extra',
                       'markdown.extensions.codehilite',
                       'markdown.extensions.toc']
         )
    return md.convert(self.content)


class Answer(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  content = MDTextField()
  uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
  total_votes = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  is_answer = models.BooleanField(default=False)
  votes = GenericRelation(Vote)

  class Meta:
    ordering = ["-is_answer", "-created_at"]
    verbose_name = _("Answer")
    verbose_name_plural = _("Answers")
  def __str__(self):
    return self.content

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
    Answer.objects.filter(uuid_id=self.uuid_id).update(
        total_votes=dic[True] - dic[False]
    )
    self.refresh_from_db()

  def get_upvoters(self):
    return [vote.user for vote in self.votes.filter(value=True)]
  def get_downvoters(self):
    return [vote.user for vote in self.votes.filter(value=False)]

  def accept_answer(self):
    answer_set = Answer.objects.filter(question=self.question)
    answer_set.update(is_answer=False)
    self.is_answer = True
    self.save()
    self.question.has_answer = True
    self.question.save()
