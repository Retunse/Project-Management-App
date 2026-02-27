from django.shortcuts import render, get_object_or_404
from .models import Board

def board_list(request):
    # fetch all boards from the database to display them on the homepage
    boards = Board.objects.all()
    return render(request, 'boards/board_list.html', {'boards': boards})

def board_detail(request, slug):
    # fetch the board by slug and pre-load lists and their tasks in one go
    board = get_object_or_404(Board.objects.prefetch_related('lists__tasks'), slug=slug)
    return render(request, 'boards/board_detail.html', {'board': board})