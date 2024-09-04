from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include("polls.urls")),
    path('', include("make_menu.urls")),
]