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
from article import views

app_name = 'article'
urlpatterns = [
    path('', views.index, name='index'),
    path('article_edit/', views.article_edit, name='article_edit'),
    path('article_edit/<int:id>/', views.article_edit, name='article_edit'),
    path('article_delete/<int:id>/', views.article_delete, name='article_delete'),
    re_path(r'^(?P<category_slug>[\w\_]+)/$', views.category, name='category'),
    re_path(r'^(?P<category_slug>[\w\_]+)/(?P<article_pk>[0-9]+)/$', views.article_detail, name='article_detail'),
]
