from django.urls import path

from . import views

app_name = "players"
urlpatterns = [
    path("", views.index, name="index"),
    path("duos/", views.select_duo, name="select_duo"),
    path("<str:username>/", views.view_player, name="view_player"),
    path("<str:username1>/<str:username2>/", views.view_duo, name="view_duo"),
]
