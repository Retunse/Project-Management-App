from django import forms
from .models import Task

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