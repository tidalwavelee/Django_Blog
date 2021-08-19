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
from event import views

app_name = 'event'
urlpatterns = [
    re_path(r"^$", views.QuestionListView.as_view(), name="index_all"),
    re_path(
        r"^event-detail/(?P<pk>\d+)/$",
        views.EventDetailView.as_view(),
        name="event_detail",
    ),
    re_path(r"^post_event/$", views.CreateEventView.as_view(), name="post_event"),
    re_path(r"^event/vote/$", views.event_vote, name="event_vote"),
]
