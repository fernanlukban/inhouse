from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.view_player, name='view_player'),
]
