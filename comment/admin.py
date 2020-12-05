from django.contrib import admin
from comment.models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object','created_at','body','user')
