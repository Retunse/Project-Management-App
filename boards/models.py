from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Board(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # generate a unique slug based on the title before saving
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

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

    class Meta:
        # newest tasks appear first
        ordering = ['-created_at']

    def __str__(self):
        return self.title