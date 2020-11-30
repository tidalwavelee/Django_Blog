from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from article.models import Category,Article,UserProfile
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

# define an inline admin descriptor for UserProfile model
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'
# Define a new UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
