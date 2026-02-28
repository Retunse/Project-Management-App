from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Board(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def save(self, *args, **kwargs):
        # generate a unique slug based on the title before saving
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Label(models.Model):
    COLOR_CHOICES = [
        ('bg-green-500', 'Green'),
        ('bg-yellow-500', 'Yellow'),
        ('bg-orange-500', 'Orange'),
        ('bg-red-500', 'Red'),
        ('bg-purple-500', 'Purple'),
        ('bg-blue-500', 'Blue'),
    ]
    title = models.CharField(max_length=50)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='bg-green-500')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='labels')

    def __str__(self):
        return self.title

class List(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')
    title = models.CharField(max_length=100)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        # sort lists by their position field
        ordering = ['position']

    def __str__(self):
        return f"{self.board.title} - {self.title}"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MED', 'Medium'),
        ('HIGH', 'High'),
    ]

    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=4, choices=PRIORITY_CHOICES, default='MED')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label, blank=True, related_name='tasks')
    position = models.PositiveIntegerField(default=0)

    class Meta:
        # newest tasks appear first
        ordering = ['position']

    def __str__(self):
        return self.title

class ActivityLog(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # the text describing what happened
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # newest activities first
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.message}"