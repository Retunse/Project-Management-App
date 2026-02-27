from django.contrib import admin
from .models import Board, List, Task

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    # automatically fill the slug field based on the title
    prepopulated_fields = {'slug': ('title',)}

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'position')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'priority', 'due_date')
    list_filter = ('priority', 'list__board')