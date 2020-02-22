from django.urls import path

from . import views

app_name = "reddit"

urlpatterns = [
    path("search/", views.search, name="search"),
]
