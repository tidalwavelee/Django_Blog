from django.contrib import admin
from article.models import Category,Article
#from mdeditor.widgets import MDEditorWidget
#from django.db import models

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
#    list_display = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
#    formfield_overrides = {
#      models.TextField: {'widget': MDEditorWidget}
#    }
    list_display = ('title','category','author','read','created_at','updated_at')

