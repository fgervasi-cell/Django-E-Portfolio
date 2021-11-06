from django.shortcuts import render, redirect
from .models import TodoItem


# Create your views here.
def list_view(request):
    todo_items = TodoItem.objects.filter(done=False).order_by('due_date')
    todo_items_done = TodoItem.objects.filter(done=True).order_by('due_date')
    context = {
        'todo_items': todo_items,
        'todo_items_done': todo_items_done
    }
    return render(request, 'todo_app/list-view.html', context)


def delete(request, todo_id):
    TodoItem.objects.filter(id=todo_id).delete()
    return redirect('list-view')


def update(request, todo_id):
    item = TodoItem.objects.get(id=todo_id)
    item.done = not item.done
    item.save()
    return redirect('list-view')


def create_page(request):
    return render(request, 'todo_app/create-task.html')


def create(request):
    _title = request.POST.get('title', 'Title')
    _description = request.POST.get('description', 'Description')
    _due_date = request.POST.get('due-date', '1970-01-01 00:00')
    todo = TodoItem(title=_title, description=_description,
                    due_date=_due_date)
    todo.save()
    return redirect('list-view')
