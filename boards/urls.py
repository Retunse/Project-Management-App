from django.urls import path
from . import views

urlpatterns = [
    path('', views.board_list, name='board_list'),
    path('board/create/', views.create_board, name='create_board'),

    path('board/<slug:slug>/', views.board_detail, name='board_detail'),
    path('board/<int:board_id>/add-list/', views.add_list, name='add_list'),
    path('list/<int:list_id>/add-task/', views.add_task, name='add_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('signup/', views.signup, name='signup'),
    path('board/<slug:slug>/delete/', views.delete_board, name='delete_board'),
    path('list/<int:list_id>/delete/', views.delete_list, name='delete_list'),
    path('board/<slug:slug>/edit/', views.edit_board, name='edit_board'),
    path('list/<int:list_id>/edit/', views.edit_list, name='edit_list'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('board/<slug:slug>/labels/', views.manage_labels, name='manage_labels'),
    path('task/<int:task_id>/update-labels/', views.update_task_labels, name='update_task_labels'),
    path('tasks/update-order/', views.update_task_order, name='update_task_order'),
    path('lists/update-order/', views.update_list_order, name='update_list_order'),
    path('boards/update-order/', views.update_board_order, name='update_board_order'),
    path('board/<slug:slug>/add-member/', views.add_member, name='add_member'),
    path('task/<int:task_id>/assign/', views.assign_task, name='assign_task'),
    path('task/<int:task_id>/checklist/add/', views.add_checklist_item, name='add_checklist_item'),
    path('checklist/toggle/<int:item_id>/', views.toggle_checklist_item, name='toggle_checklist_item'),
]