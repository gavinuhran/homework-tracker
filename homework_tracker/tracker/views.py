from django.shortcuts import render
from .models import Task
import datetime

id = 0

# Create your views here.
def index(request):
    tasks = sorted(Task.objects.all(), key=lambda x: x.due_date)
    return render(request, 'index.html', {'tasks': tasks})

def create(request):
    if request.method == 'POST':
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
    else:
        return render(request, 'create.html', {})

def delete(request):
    if request.method == 'POST':
        id = int(request.POST.get('id'))
        for task in Task.objects.all():
            if task.id == id:
                task.delete()
                return render(request, 'delete.html', {})
        return render(request, 'delete_error.html', {})
        
    else:
        return render(request, 'delete.html', {})

def update(request):
    global id
    if request.method == 'POST':
        if request.POST['action'] == 'id':
            id = int(request.POST.get('id'))
            for task in Task.objects.all():
                if task.id == id:
                    task = Task.objects.get(id=id)
                    date = datetime.date.strftime(task.due_date, "%m/%d/%Y")
                    return render(request, 'update.html', {'task': task, 'date': date})
            return render(request, 'id_error.html', {})

            
        elif request.POST['action'] == 'update':
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
    else:
        return render(request, 'id.html', {})