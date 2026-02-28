from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, List, Task, User, Label, ActivityLog
from .forms import TaskForm, BoardForm, ListForm, SignUpForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def log_activity(user, board, message):
    """ Helper function to record user actions on the board """
    ActivityLog.objects.create(user=user, board=board, message=message)

@login_required
def board_list(request):
    # filter boards to show only those belonging to the current user
    boards = Board.objects.filter(owner=request.user)
    return render(request, 'boards/board_list.html', {'boards': boards})

@login_required
def board_detail(request, slug):
    # display board details and associated lists/tasks
    board = get_object_or_404(Board, slug=slug, owner=request.user)
    return render(request, 'boards/board_detail.html', {'board': board})

@login_required
def add_task(request, list_id):
    # get the specific list where the task will be added
    target_list = get_object_or_404(List, id=list_id, board__owner=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        # quick add logic (only title from inline form)
        if title:
            task = Task.objects.create(title=title, list=target_list)
            log_activity(request.user, target_list.board, f"added card '{task.title}' to {target_list.title}")
            return redirect('board_detail', slug=target_list.board.slug)

        # full form logic (with description and priority)
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.list = target_list
            task.save()
            log_activity(request.user, target_list.board, f"added card '{task.title}' to {target_list.title}")
            return redirect('board_detail', slug=target_list.board.slug)
    else:
        form = TaskForm()

    return render(request, 'boards/add_task.html', {'form': form, 'target_list': target_list})

@login_required
@require_POST
def delete_task(request, task_id):
    # find task and ensure owner has permission through list/board
    task = get_object_or_404(Task, id=task_id, list__board__owner=request.user)
    board = task.list.board
    task_title = task.title
    task.delete()
    log_activity(request.user, board, f"deleted card '{task_title}'")
    return redirect('board_detail', slug=board.slug)

@login_required
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            log_activity(request.user, board, f"created the board '{board.title}'")
            return redirect('board_detail', slug=board.slug)
    else:
        form = BoardForm()
    return render(request, 'boards/create_board.html', {'form': form})

@login_required
def add_list(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)

    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.board = board
            # auto-positioning logic
            current_lists_count = board.lists.count()
            new_list.position = current_lists_count + 1
            new_list.save()
            log_activity(request.user, board, f"added list '{new_list.title}'")
            return redirect('board_detail', slug=board.slug)
    else:
        form = ListForm()
    return render(request, 'boards/add_list.html', {'form': form, 'board': board})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('board_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
@require_POST
def delete_board(request, slug):
    board = get_object_or_404(Board, slug=slug, owner=request.user)
    board.delete()
    # no log after deletion because the board no longer exists
    return redirect('board_list')

@login_required
@require_POST
def delete_list(request, list_id):
    list_obj = get_object_or_404(List, id=list_id, board__owner=request.user)
    board = list_obj.board
    list_title = list_obj.title
    list_obj.delete()
    log_activity(request.user, board, f"deleted list '{list_title}'")
    return redirect('board_detail', slug=board.slug)

@login_required
def edit_board(request, slug):
    board = get_object_or_404(Board, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            log_activity(request.user, board, f"renamed board to '{board.title}'")
            return redirect('board_list')
    else:
        form = BoardForm(instance=board)
    return render(request, 'boards/edit_board.html', {'form': form, 'board': board})

@login_required
def edit_list(request, list_id):
    list_obj = get_object_or_404(List, id=list_id, board__owner=request.user)
    if request.method == 'POST':
        form = ListForm(request.POST, instance=list_obj)
        if form.is_valid():
            form.save()
            log_activity(request.user, list_obj.board, f"renamed list to '{list_obj.title}'")
            return redirect('board_detail', slug=list_obj.board.slug)
    else:
        form = ListForm(instance=list_obj)
    return render(request, 'boards/edit_list.html', {'form': form, 'list': list_obj})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, list__board__owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            log_activity(request.user, task.list.board, f"edited card '{task.title}'")
            return redirect('board_detail', slug=task.list.board.slug)
    else:
        form = TaskForm(instance=task)
    return render(request, 'boards/edit_task.html', {'form': form, 'task': task})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, list__board__owner=request.user)
    return render(request, 'boards/task_detail.html', {'task': task})

@login_required
def manage_labels(request, slug):
    board = get_object_or_404(Board, slug=slug, owner=request.user)
    labels = board.labels.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        color = request.POST.get('color')
        if title and color:
            label = Label.objects.create(title=title, color=color, board=board)
            log_activity(request.user, board, f"created new label '{label.title}'")
            return redirect('manage_labels', slug=slug)

    return render(request, 'boards/manage_labels.html', {'board': board, 'labels': labels})

@login_required
@require_POST
def update_task_labels(request, task_id):
    task = get_object_or_404(Task, id=task_id, list__board__owner=request.user)
    label_ids = request.POST.getlist('labels')
    task.labels.set(label_ids)
    log_activity(request.user, task.list.board, f"updated labels for card '{task.title}'")
    return redirect('task_detail', task_id=task.id)