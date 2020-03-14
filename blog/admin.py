from django.contrib import admin
from blog.models import Category,Article

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
#    list_display = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('category','title','author','publish_date','last_updated_time','slug')
