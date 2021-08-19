from django.contrib import admin
from event.models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
  list_display = ("title","user","created_at","area_code","votes")
