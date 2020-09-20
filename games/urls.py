from django.urls import path

from . import views

app_name = "games"

urlpatterns = [
    path("upload/", views.upload_match_history, name="upload_match_history"),
    path("", views.show_games, name="show_games"),
]
