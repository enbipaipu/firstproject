from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/chat", views.detail, name="chat"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/addchoice/", views.addchoice, name="addchoice"), #追加箇所
]