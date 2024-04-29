from django.shortcuts import render, redirect  # Importing necessary libraries
# Importing necessary libraries
from django.contrib.auth.decorators import login_required
from .models import Task  # Importing necessary libraries
from .queues import TaskPriorityQueue  # Importing necessary libraries
from .forms import TaskForm  # Importing necessary libraries


@login_required
def display_queue(request):
    # Creating an instance of TaskPriorityQueue for the current user
    queue = TaskPriorityQueue(request.user)
    queue.sort_queue()  # Sorting the queue
    # Extracting tasks from the queue
    tasks = [node.get_task() for node in queue.queue]
    # Rendering the template with tasks
    return render(request, 'todolistapp/display_queue.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')  # Getting the title from the request
        # Convert priority to integer
        # Getting the priority from the request and converting it to an integer
        priority = int(request.POST.get('priority'))
        # Getting the deadline from the request
        deadline = request.POST.get('deadline')
        Task.objects.create(
            title=title,
            priority=priority,  # Use the integer value as the priority
            deadline=deadline,
            user=request.user
        )
        # Redirecting to the display_queue view
        return redirect('display_queue')
    else:
        form = TaskForm()
    # Rendering the template with the form
    return render(request, 'todolistapp/add_task.html', {'form': form})


@login_required
def delete_task(request, task_id):
    # Creating an instance of TaskPriorityQueue for the current user
    queue = TaskPriorityQueue(request.user)

    # Getting the task to delete from the database
    try:
        task_to_delete = Task.objects.raw(
            'SELECT * FROM todolistapp_task WHERE id = %s', [task_id])[0]
    except IndexError:
        raise Task.DoesNotExist("Task with id {} does not exist.".format(task_id))
    queue.remove_task_by_id(task_id)  # Removing the task from the queue
    task_to_delete.delete()  # Deleting the task from the database
    queue.save_tasks_to_db()  # Saving the updated queue to the database
    return redirect('display_queue')  # Redirecting to the display_queue view
