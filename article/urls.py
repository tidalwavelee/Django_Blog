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
    path('add_article/', views.add_article, name='add_article'),
    path('<slug:category_slug>/', views.category, name='category'),
    re_path(r'^([\w\-]+)/(?P<article_pk>[0-9]+)/$', views.article, name='article'),
]