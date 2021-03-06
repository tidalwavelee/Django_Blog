"""opencads URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,re_path
from userprofile import views

app_name = 'userprofile'
urlpatterns = [
    path('user_delete/<int:id>/', views.user_delete, name='user_delete'),
    path('profile_detail/<int:id>/', views.profile_detail, name='profile_detail'),
    path('profile_edit/<int:id>/', views.profile_edit, name='profile_edit'),
    path('set_following/', views.set_following, name='set_following'),
    path('unfollow/', views.unfollow, name='unfollow'),
    path('add_favorite/', views.add_favorite, name='add_favorite'),
    path('del_favorite/', views.del_favorite, name='del_favorite'),
]
