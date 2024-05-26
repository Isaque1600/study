from django.contrib import admin
from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.VoteView.as_view(), name="vote"),
    path("create/", views.QuestionsView.as_view(), name="question_create"),
    path(
        "create_choices/<int:question_id>/",
        views.ChoiceView.as_view(),
        name="choice_create",
    ),
]
