from django.shortcuts import render
from .models import Task, TimeEntry
import datetime

id = 0
start_time = None

# Create your views here.
def index(request):
    # Renders home page
    tasks = sorted(Task.objects.all(), key=lambda x: x.due_date)
    return render(request, 'index.html', {'tasks': tasks})

def create(request):
    
    if request.method == 'POST': # When user clicks "Create Assignment" button, a new task is created and saved in the local database
        task = Task()
        task.title = request.POST.get('title')
        task.project = request.POST.get('project')

        # nums = [MM, DD, YYYY]
        nums = [int(x) for x in request.POST.get('date').split('/')]
        d = datetime.date(nums[2], nums[0], nums[1])
        task.due_date = d

        task.description = request.POST.get('description')
        task.status = request.POST.get('status')
        task.total_time = request.POST.get('total_time')
        task.save()

        return render(request, 'create.html', {})
    else: # Otherwise the form is continually rendered as the user enters data for a task
        return render(request, 'create.html', {})

def delete(request):
    if request.method == 'POST': # When user clicks "Delete Assignment", the given task_id is deleted from the local database
        id = int(request.POST.get('id'))
        for task in Task.objects.all():
            if task.id == id:
                task.delete()
                return render(request, 'delete.html', {})

        return render(request, 'delete_error.html', {}) # If user enters an invalid ID an error message is displayed
        
    else: # Otherwise the form is continually rendered as the user enters data for a task to be deleted
        return render(request, 'delete.html', {})

def update(request):
    global id
    if request.method == 'POST': 
        if request.POST['action'] == 'id': # When the user clicks the "View Assignment" button, the page that allows the user to update the data for a given task_id is rendered
            id = int(request.POST.get('id'))
            for task in Task.objects.all():
                if task.id == id:
                    task = Task.objects.get(id=id)
                    date = datetime.date.strftime(task.due_date, "%m/%d/%Y")
                    return render(request, 'update.html', {'task': task, 'date': date}) # Renders the form for the given task_id with the field prefilled with the task data

            return render(request, 'id_error.html', {}) # Displays an error message if an incorrect id is given

            
        elif request.POST['action'] == 'update': # When the user clicks the "Update Assignment" button, the task is saved with the new given data
            task = Task.objects.get(id=id)
            task.title = request.POST.get('title')
            task.project = request.POST.get('project')

            # nums = [MM, DD, YYYY]
            nums = [int(x) for x in request.POST.get('date').split('/')]
            d = datetime.date(nums[2], nums[0], nums[1])
            task.due_date = d

            task.description = request.POST.get('description')
            task.status = request.POST.get('status')
            task.total_time = request.POST.get('total_time')
            task.save()

            return render(request, 'update.html', {})
    else: # Otherwise the form is continually rendered as the user enters data for a task_id to be updated
        return render(request, 'id.html', {})

def timer(request):
    global start_time
    task = None
    global id

    if request.method == 'POST':
        if request.POST['action'] == 'id': # When the user clicks the "View Assignment" button, the page that allows the user to update the data for a given task_id is rendered
            id = int(request.POST.get('id'))
            for task in Task.objects.all():
                if task.id == id:
                    task = Task.objects.get(id=id)
                    return render(request, 'timer.html', {'task': task, 'state': 0}) # State 0 = start state

            return render(request, 'id_error.html', {}) # Displays an error message if an incorrect id is given

        elif request.POST['action'] == 'start':
            start_time = datetime.datetime.now()
            return render(request, 'timer.html', {'task': task, 'state': 1}) # After hitting start, state 1 = timer running state
            
        elif request.POST['action'] == 'stop':
            time_entry = TimeEntry()
            time_entry.start_time = start_time
            time_entry.end_time = datetime.datetime.now()
            time_entry.task = id
            time_entry.save()

            return render(request, 'timer.html', {'task': task, 'state': 2}) # After stopping the timer, state 2 = timer ended state
    else:
        return render(request, 'id.html', {})