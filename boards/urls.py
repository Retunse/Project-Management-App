from django.urls import path
from . import views

urlpatterns = [
    path('', views.board_list, name='board_list'),
    # dynamic route for viewing a specific board using its unique slug
    path('board/<slug:slug>/', views.board_detail, name='board_detail'),
    path('list/<int:list_id>/add-task/', views.add_task, name='add_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
]