from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>",views.entry, name="entry"),
    path("search", views.search , name="search"),
    path("newpage",views.newpage, name="newpage"),
    path("randompage",views.randompage, name="randompage"),
    path("savenewpage", views.savenewpage, name="savenewpage"),
    path("edit", views.edit, name="edit")
]
