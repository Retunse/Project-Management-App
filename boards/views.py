from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, List, Task, User, Label, ActivityLog, ChecklistItem, Comment
from .forms import TaskForm, BoardForm, ListForm, SignUpForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.db.models import Q

def log_activity(user, board, message):
    """ Helper function to record user actions on the board """
    ActivityLog.objects.create(user=user, board=board, message=message)

def get_board_with_access(slug, user):
    return get_object_or_404(Board, Q(slug=slug) & (Q(owner=user) | Q(members=user)))

@login_required
def board_list(request):
    # filter boards to show only those belonging to the current user
    boards = Board.objects.filter(
        Q(owner=request.user) | Q(members=request.user)
    ).prefetch_related('members', 'owner').distinct().order_by('position')
    return render(request, 'boards/board_list.html', {'boards': boards})

@login_required
def board_detail(request, slug):
    # display board details and associated lists/tasks
    board = get_object_or_404(
        Board,
        Q(owner=request.user) | Q(members=request.user),
        slug=slug
    )
    return render(request, 'boards/board_detail.html', {'board': board})

@login_required
def add_task(request, list_id):
    # get the specific list where the task will be added
    target_list = get_object_or_404(List, id=list_id, board__in=Board.objects.filter(Q(owner=request.user) | Q(members=request.user)))

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            task = Task.objects.create(title=title, list=target_list)
            log_activity(request.user, target_list.board, f"added card '{task.title}' to {target_list.title}")
            return redirect('board_detail', slug=target_list.board.slug)

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
    board = get_object_or_404(Board, Q(id=board_id) & (Q(owner=request.user) | Q(members=request.user)))

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
    task = get_object_or_404(Task, id=task_id, list__board__in=Board.objects.filter(Q(owner=request.user) | Q(members=request.user)))
    board = task.list.board

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, board=board)
        if form.is_valid():
            form.save()
            log_activity(request.user, board, f"edited details of card '{task.title}'")
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'boards/edit_task.html', {'form': form, 'task': task})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, list__board__in=Board.objects.filter(Q(owner=request.user) | Q(members=request.user)))

    items = task.checklist_items.all()
    total = items.count()
    completed = items.filter(is_done=True).count()
    progress = int((completed / total) * 100) if total > 0 else 0
    return render(request, 'boards/task_detail.html', {
        'task': task,
        'progress': progress
    })

@login_required
def manage_labels(request, slug):
    board = get_object_or_404(Board, Q(slug=slug) & (Q(owner=request.user) | Q(members=request.user)))
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
    task = get_object_or_404(
        Task,
        id=task_id,
        list__board__in=Board.objects.filter(Q(owner=request.user) | Q(members=request.user))
    )
    label_ids = request.POST.getlist('labels')
    task.labels.set(label_ids)
    log_activity(request.user, task.list.board, f"updated labels for card '{task.title}'")
    return redirect('task_detail', task_id=task.id)


@login_required
@require_POST
def update_task_order(request):
    """
    Handle drag and drop reordering of tasks.
    Updates both the list assignment and the vertical position within the list.
    """
    new_list_id = request.POST.get('list_id')
    task_ids_str = request.POST.get('task_ids')

    if task_ids_str and new_list_id:
        # Convert comma-separated string of IDs from JavaScript to a Python list
        task_ids = task_ids_str.split(',')

        # Ensure the new list exists and belongs to the current user's board
        new_list = get_object_or_404(List, id=new_list_id, board__owner=request.user)

        # use a transaction-like approach by updating each tasks position based on its index in the received array
        for index, t_id in enumerate(task_ids):
            # filter by ID and board owner for extra security
            task_query = Task.objects.filter(id=t_id, list__board__owner=request.user)

            if task_query.exists():
                task = task_query.first()
                old_list = task.list

                # Update task's list and its new position index
                task_query.update(list=new_list, position=index)

        # Final log for the movement action
        log_activity(request.user, new_list.board, f"reordered tasks in {new_list.title}")

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)


@login_required
@require_POST
def update_list_order(request):
    """ Handle drag and drop reordering for lists within a board """
    list_ids_str = request.POST.get('list_ids')
    if list_ids_str:
        list_ids = list_ids_str.split(',')
        for index, l_id in enumerate(list_ids):
            List.objects.filter(id=l_id, board__owner=request.user).update(position=index)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@require_POST
def update_board_order(request):
    """ Handle drag and drop reordering for boards on the dashboard """
    board_ids_str = request.POST.get('board_ids')
    if board_ids_str:
        board_ids = board_ids_str.split(',')
        for index, b_id in enumerate(board_ids):
            Board.objects.filter(id=b_id, owner=request.user).update(position=index)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def add_member(request, slug):
    """ Allow board owner to add other users as members """
    board = get_object_or_404(Board, slug=slug, owner=request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user_to_add = User.objects.get(username=username)
            if user_to_add != board.owner:
                board.members.add(user_to_add)
                log_activity(request.user, board, f"added {username} to the board")
        except User.DoesNotExist:
                pass

    return redirect('board_detail', slug=slug)

@login_required
@require_POST
def assign_task(request, task_id):
    # Fetch task if user has access to the board
    task = get_object_or_404(Task, Q(id=task_id) & (
                Q(list__board__owner=request.user) | Q(list__board__members=request.user)))
    user_id = request.POST.get('user_id')

    if user_id:
        assigned_user = get_object_or_404(User, id=user_id)
        task.assigned_to = assigned_user
        message = f"assigned '{task.title}' to {assigned_user.username}"
    else:
        task.assigned_to = None
        message = f"removed assignment from '{task.title}'"

    task.save()
    log_activity(request.user, task.list.board, message)
    return redirect('task_detail', task_id=task.id)

@login_required
@require_POST
def add_checklist_item(request, task_id):
    task = get_object_or_404(Task, id=task_id, list__board__in=Board.objects.filter(Q(owner=request.user) | Q(members=request.user)))
    title = request.POST.get('title')
    if title:
        ChecklistItem.objects.create(task=task, title=title)
    return redirect('task_detail', task_id=task.id)

@login_required
@require_POST
def toggle_checklist_item(request, item_id):
    item = get_object_or_404(ChecklistItem, id=item_id, task__list__board__in=Board.objects.filter(Q(owner=request.user) | Q(members=request.user)))
    item.is_done = not item.is_done
    item.save()
    return redirect('task_detail', task_id=item.task.id)


@login_required
@require_POST
def add_comment(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        list__board__in=Board.objects.filter(Q(owner=request.user) | Q(members=request.user))
    )
    text = request.POST.get('text')
    if text:
        Comment.objects.create(task=task, author=request.user, text=text)
        log_activity(request.user, task.list.board, f"commented on '{task.title}'")

    return redirect('task_detail', task_id=task.id)

@login_required
def archive_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        list__board__in=Board.objects.filter(Q(owner=request.user) | Q(members=request.user))
    )
    task.is_archived = True
    task.save()
    log_activity(request.user, task.list.board, f"archived card '{task.title}'")
    return redirect('board_detail', slug=task.list.board.slug)


@login_required
def board_archive(request, slug):
    board = get_object_or_404(Board, Q(slug=slug) & (Q(owner=request.user) | Q(members=request.user)))
    archived_tasks = Task.objects.filter(list__board=board, is_archived=True).order_by('-due_date')

    return render(request, 'boards/archive.html', {
        'board': board,
        'tasks': archived_tasks
    })


@login_required
def unarchive_task(request, task_id):
    task = get_object_or_404(Task, id=task_id,
                             list__board__in=Board.objects.filter(Q(owner=request.user) | Q(members=request.user)))
    task.is_archived = False
    task.save()
    log_activity(request.user, task.list.board, f"restored card '{task.title}' from archive")
    return redirect('task_detail', task_id=task.id)