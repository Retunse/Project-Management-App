from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, List
from .forms import TaskForm

def board_list(request):
    # fetch all boards from the database to display them on the homepage
    boards = Board.objects.all()
    return render(request, 'boards/board_list.html', {'boards': boards})

def board_detail(request, slug):
    # fetch the board by slug and pre-load lists and their tasks in one go
    board = get_object_or_404(Board.objects.prefetch_related('lists__tasks'), slug=slug)
    return render(request, 'boards/board_detail.html', {'board': board})


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