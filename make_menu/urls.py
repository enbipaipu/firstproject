from django.urls import path

from . import views

app_name = "make_menu"
urlpatterns = [
   path("", views.index, name="index"),
   path("result/", views.result, name="result"),

   path("read_csv/", views.read_csv, name="read_csv"),

   path('scrape/', views.scrape, name='scrape'),

]

