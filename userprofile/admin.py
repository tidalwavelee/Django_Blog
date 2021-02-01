from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from userprofile.models import Profile, FollowRelation, Favorite

# define an inline admin descriptor for UserProfile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'
# Define a new UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User,UserAdmin)


@admin.register(FollowRelation)
class FollowRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'followed','following','created_at')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','content_object','created_at')
