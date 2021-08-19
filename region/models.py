from django.db import models
from django.utils.translation import ugettext_lazy as _

class Region(models.Model):
  country = models.CharField(max_length=60)
  province = models.CharField(max_length=60)
  city = models.CharField(max_length=60)
  county = models.CharField(max_length=60, null=True, black=True)
  longitude = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
  latitude = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
  zip_code = models.CharField(max_length=6, null=True, blank=True)

  class Meta:
    ordering = ["-province"]
    verbose_name = _("Region")
    verbose_name_plural = _("Regions")

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
  def __str__(self):
    return f"{self.province}-{self.city}-{self.county}"
