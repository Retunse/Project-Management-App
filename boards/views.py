from django.shortcuts import render
from .models import Board

def board_list(request):
    # fetch all boards from the database to display them on the homepage
    boards = Board.objects.all()
    return render(request, 'boards/board_list.html', {'boards': boards})