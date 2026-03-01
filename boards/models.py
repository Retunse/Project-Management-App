from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta

class Board(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    members = models.ManyToManyField(User, related_name='joined_boards', blank=True)
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
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    due_date = models.DateTimeField(null=True, blank=True)

    @property
    def checklist_total_count(self):
        return self.checklist_items.count()

    @property
    def checklist_completed_count(self):
        return self.checklist_items.filter(is_done=True).count()

    @property
    def due_status(self):
        if not self.due_date:
            return None
        now = timezone.now()
        if self.due_date < now:
            return "overdue"
        if self.due_date < now + timedelta(days=1):
            return "soon"
        return "upcoming"

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

class ChecklistItem(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='checklist_items')
    title = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position', 'created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"