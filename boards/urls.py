from django.urls import path
from . import views

urlpatterns = [
    # route for the main page showing the list of boards
    path('', views.board_list, name='board_list'),
]