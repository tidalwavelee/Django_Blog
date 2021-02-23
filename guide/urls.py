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
from guide import views

app_name = 'guide'
urlpatterns = [
    re_path(r"^$", views.QuestionListView.as_view(), name="index_noans"),
    re_path(r"^answered/$", views.QuestionAnsListView.as_view(), name="index_ans"),
    re_path(r"^indexed/$", views.QuestionsIndexListView.as_view(), name="index_all"),
    re_path(
        r"^question-detail/(?P<pk>\d+)/$",
        views.QuestionDetailView.as_view(),
        name="question_detail",
    ),
    re_path(r"^ask-question/$", views.CreateQuestionView.as_view(), name="ask_question"),
    re_path(
        r"^propose-answer/(?P<question_id>\d+)/$",
        views.CreateAnswerView.as_view(),
        name="propose_answer",
    ),
    re_path(r"^question/vote/$", views.question_vote, name="question_vote"),
    re_path(r"^answer/vote/$", views.answer_vote, name="answer_vote"),
    re_path(r"^accept-answer/$", views.accept_answer, name="accept_answer"),
]
