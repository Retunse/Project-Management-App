from django.urls import path
from . import views

urlpatterns = [
    path('', views.board_list, name='board_list'),
    # dynamic route for viewing a specific board using its unique slug
    path('board/<slug:slug>/', views.board_detail, name='board_detail'),
]