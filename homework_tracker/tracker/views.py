from django.shortcuts import render
from .models import Task
import datetime

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
        id = request.POST.get('id')
        Task.objects.get(id=id).delete()

        tasks = sorted(Task.objects.all(), key=lambda x: x.due_date)
        return render(request, 'delete.html', {})
    else:
        return render(request, 'delete.html', {})