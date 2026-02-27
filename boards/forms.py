from django import forms
from .models import Task, Board, List

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # specify which fields should be available in the form
        fields = ['title', 'description', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded mb-2', 'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded mb-2', 'rows': 3, 'placeholder': 'Optional description'}),
            'priority': forms.Select(attrs={'class': 'w-full p-2 border rounded mb-2'}),
        }

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        # only allow editing the title
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 outline-none transition',
                'placeholder': 'Enter board title...'
            }),
        }

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        # only the title is needed from the user
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none',
                'placeholder': 'Enter list title...'
            }),
        }