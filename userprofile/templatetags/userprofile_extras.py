from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Favorite
from ..forms import FavoriteForm

register = template.Library()

@register.simple_tag
def retrieve_favorites(user):
  favorites = Favorite.objects.filter(user=user)
  objects = []
  for favorite in favorites:
    obj = favorite.content_type.get_object_for_this_type(id=favorite.object_id)
    obj.type = favorite.content_type.model_class().__name__
    obj.favID = favorite.id
    objects.append(obj)
  return objects

@register.simple_tag
def get_favorite_form(obj):
  obj_content_type = ContentType.objects.get_for_model(obj) 
  favorite_form = FavoriteForm(initial={'content_type': obj_content_type,'object_id': obj.pk})
  return favorite_form
