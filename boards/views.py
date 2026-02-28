from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, List, Task, User
from .forms import TaskForm, BoardForm, ListForm, SignUpForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

@login_required
def board_list(request):
    # fetch all boards from the database to display them on the homepage
    boards = Board.objects.all()
    return render(request, 'boards/board_list.html', {'boards': boards})

@login_required
def board_detail(request, slug):
    # fetch the board by slug and pre-load lists and their tasks in one go
    board = get_object_or_404(Board.objects.prefetch_related('lists__tasks'), slug=slug)
    return render(request, 'boards/board_detail.html', {'board': board})

@login_required
def add_task(request, list_id):
    # get the specific list where the task will be added
    target_list = get_object_or_404(List, id=list_id)

    if request.method == 'POST':
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
            board.owner = User.objects.first()
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