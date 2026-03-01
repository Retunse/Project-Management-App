from django import forms
from .models import Task, Board, List, User
from django.contrib.auth.forms import UserCreationForm

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

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # define the css classes for all inputs
            css_classes = 'w-full p-3 bg-white border-2 border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all text-gray-800'
            for field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': css_classes
                })

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-lg border-2 border-gray-100 focus:border-blue-500 outline-none transition',
                'placeholder': 'Task Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-3 rounded-lg border-2 border-gray-100 focus:border-blue-500 outline-none transition',
                'rows': 4,
                'placeholder': 'Add a more detailed description...'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full p-3 rounded-lg border-2 border-gray-100 focus:border-blue-500 outline-none transition cursor-pointer'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full p-3 rounded-lg border-2 border-gray-100 focus:border-blue-500 outline-none transition'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'w-full p-3 rounded-lg border-2 border-gray-100 focus:border-blue-500 outline-none transition cursor-pointer'
            }),
        }

    def __init__(self, *args, **kwargs):
        board = kwargs.pop('board', None)
        super().__init__(*args, **kwargs)
        if board:
            self.fields['assigned_to'].queryset = User.objects.filter(
                id__in=[board.owner.id] + [m.id for m in board.members.all()]
            )