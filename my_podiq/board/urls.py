from django.urls import path
from . import views

urlpatterns = [
    path('', views.board_home, name='board_home'),
    path('create', views.create, name='create')
]