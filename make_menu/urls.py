from django.urls import path
from . import views

app_name = "make_menu"
urlpatterns = [
   path("", views.index, name="index"),
   path("result/", views.result, name="result"),
   path("read_csv/", views.read_csv, name="read_csv"),
   path('db/create/', views.create, name='create'),
   path('db/add/', views.add_text, name='add_text'),
   path('db/read/', views.read_text, name='read_text'),
   path('scrape/', views.scrape, name='scrape'),

]
