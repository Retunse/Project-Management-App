from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, List, Task, User, Label
from .forms import TaskForm, BoardForm, ListForm, SignUpForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

@login_required
def board_list(request):
    # filter boards to show only those belonging to the current user
    boards = Board.objects.filter(owner=request.user)
    return render(request, 'boards/board_list.html', {'boards': boards})

@login_required
def board_detail(request, slug):
    board = get_object_or_404(Board, slug=slug, owner=request.user)
    return render(request, 'boards/board_detail.html', {'board': board})

@login_required
def add_task(request, list_id):
    # get the specific list where the task will be added
    target_list = get_object_or_404(List, id=list_id, board__owner=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title, list=target_list)
            return redirect('board_detail', slug=target_list.board.slug)

        form = TaskForm(request.POST)
        if form.is_valid():
            # create task object but dont save to db yet
            task = form.save(commit=False)
            task.list = target_list
            task.save()
            # redirect back to the board detail page using board slug
            return redirect('board_detail', slug=target_list.board.slug)
    else:
        # initialize an empty form for GET requests to avoid UnboundLocalError
        form = TaskForm()

    # if its a GET request just show the form
    return render(request, 'boards/add_task.html', {'form': form, 'target_list': target_list})

@require_POST
def delete_task(request, task_id):
    # find the task or return 404 if it does not exist
    task = get_object_or_404(Task, id=task_id)
    board_slug = task.list.board.slug
    # delete the task from the database
    task.delete()
    # go back to the board detail page
    return redirect('board_detail', slug=board_slug)

@login_required
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            # create board instance but don't save yet to assign the owner
            board = form.save(commit=False)
            # temporarily assign the first user as owner
            board.owner = request.user
            board.save()
            # redirect to the newly created board
            return redirect('board_detail', slug=board.slug)
    else:
        # initialize empty board form
        form = BoardForm()

    return render(request, 'boards/create_board.html', {'form': form})

@login_required
def add_list(request, board_id):
    # fetch the board where the new list will be created
    board = get_object_or_404(Board, id=board_id)

    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.board = board
            # set the position to be the last one in the board
            current_lists_count = board.lists.count()
            new_list.position = current_lists_count + 1
            new_list.save()
            return redirect('board_detail', slug=board.slug)
    else:
        form = ListForm()

    return render(request, 'boards/add_list.html', {'form': form, 'board': board})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # save the user and log them in automatically
            user = form.save()
            login(request, user)
            return redirect('board_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
@require_POST
def delete_board(request, slug):
    # find the board and ensure the logged-in user is the owner
    board = get_object_or_404(Board, slug=slug, owner=request.user)
    board.delete()
    return redirect('board_list')

@login_required
@require_POST
def delete_list(request, list_id):
    # find the list through the board owner for security
    list_obj = get_object_or_404(List, id=list_id, board__owner=request.user)
    board_slug = list_obj.board.slug
    list_obj.delete()
    return redirect('board_detail', slug=board_slug)

@login_required
def edit_board(request, slug):
    board = get_object_or_404(Board, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
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
            return redirect('board_detail', slug=task.list.board.slug)
    else:
        form = TaskForm(instance=task)
    return render(request, 'boards/edit_task.html', {'form': form, 'task': task})

@login_required
def task_detail(request, task_id):
    # Fetch task and ensure it belongs to the board owner
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
            Label.objects.create(title=title, color=color, board=board)
            return redirect('manage_labels', slug=slug)

    return render(request, 'boards/manage_labels.html', {'board': board, 'labels': labels})