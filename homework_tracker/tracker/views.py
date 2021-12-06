from django.shortcuts import render
from .models import Task, TimeEntry
import datetime
import pytz

id = 0
start_time = None

utc=pytz.UTC

week_end = utc.localize(datetime.datetime.now())
week_start = week_end - datetime.timedelta(7)

month_start = utc.localize(datetime.datetime.now()).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
month_end = (month_start + datetime.timedelta(32)).replace(day=1)

# Create your views here.
def index(request):
    # Renders home page
    tasks = sorted(Task.objects.all(), key=lambda x: x.due_date)
    times = TimeEntry.objects.all()
    time_elapsed = {}
    for time in times:
        time_elapsed[time] = (time.end_time - time.start_time)
    return render(request, 'index.html', {'tasks': tasks, 'times': times, 'time_elapsed': time_elapsed})

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
        for time in TimeEntry.objects.all():
            if time.task == id:
                time.delete()
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

            duration = time_entry.end_time - time_entry.start_time
            seconds = duration.total_seconds()
            hours = int(divmod(seconds, 3600)[0])
            minutes = int(divmod(seconds, 60)[0])
            seconds = int(seconds % 60)

            if hours:
                time_entry.time_elapsed = f'{hours} hours, {minutes} minutes, {seconds} seconds'
            elif minutes:
                time_entry.time_elapsed = f'{minutes} minutes, {seconds} seconds'
            else:
                time_entry.time_elapsed = f'{seconds} seconds'

            time_entry.task = id
            time_entry.task_title = Task.objects.get(id=id).title
            time_entry.save()

            return render(request, 'timer.html', {'task': task, 'state': 2}) # After stopping the timer, state 2 = timer ended state
    else:
        return render(request, 'id.html', {})

def update_timer(request):
    global id
    if request.method == 'POST': 
        if request.POST['action'] == 'id': # When the user clicks the "View Assignment" button, the page that allows the user to update the data for a given task_id is rendered
            id = int(request.POST.get('id'))
            for time in TimeEntry.objects.all():
                if time.id == id:
                    time = TimeEntry.objects.get(id=id)
                    start = time.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                    end = time.end_time.strftime("%m/%d/%Y, %H:%M:%S")
                    return render(request, 'update_timer.html', {'time': time, 'start': start, 'end': end})

            return render(request, 'id_error.html', {}) # Displays an error message if an incorrect id is given

            
        elif request.POST['action'] == 'update': # When the user clicks the "Update Assignment" button, the task is saved with the new given data
            time = TimeEntry.objects.get(id=id)

            time.start_time = datetime.datetime.strptime(request.POST.get('start'), '%m/%d/%Y, %H:%M:%S')

            time.end_time = datetime.datetime.strptime(request.POST.get('end'), '%m/%d/%Y, %H:%M:%S')

            if time.end_time < time.start_time:
                time = TimeEntry.objects.get(id=id)
                start = time.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                end = time.end_time.strftime("%m/%d/%Y, %H:%M:%S")
                return render(request, 'update_timer_error.html', {'time': time, 'start': start, 'end': end})
            
            duration = time.end_time - time.start_time
            seconds = duration.total_seconds()
            hours = int(divmod(seconds, 3600)[0])
            minutes = int(divmod(seconds, 60)[0])
            seconds = int(seconds % 60)

            if hours:
                time.time_elapsed = f'{hours} hours, {minutes} minutes, {seconds} seconds'
            elif minutes:
                time.time_elapsed = f'{minutes} minutes, {seconds} seconds'
            else:
                time.time_elapsed = f'{seconds} seconds'
            
            time.save()

            return render(request, 'update_timer.html', {})
    else: # Otherwise the form is continually rendered as the user enters data for a task_id to be updated
        return render(request, 'id.html', {})

def delete_timer(request):
    if request.method == 'POST': # When user clicks "Delete Assignment", the given task_id is deleted from the local database
        id = int(request.POST.get('id'))
        for time in TimeEntry.objects.all():
            if time.id == id:
                time.delete()
                return render(request, 'delete_timer.html', {})

        return render(request, 'delete_timer_error.html', {}) # If user enters an invalid ID an error message is displayed
        
    else: # Otherwise the form is continually rendered as the user enters data for a task to be deleted
        return render(request, 'delete_timer.html', {})


def time_dashboard(request):
    global week_start, week_end, month_start, month_end, utc

    if request.method == 'POST': 
        if request.POST['action'] == 'week': 
            # nums = [MM, DD, YYYY]
            nums = [int(x) for x in request.POST.get('date').split('/')]
            date = datetime.datetime(nums[2], nums[0], nums[1])
            week_start = utc.localize(date)
            week_end = week_start + datetime.timedelta(7)

        elif request.POST['action'] == 'month':
            # nums = [MM, YYYY]
            nums = [int(x) for x in request.POST.get('month').split('/')]
            month_start = utc.localize(datetime.datetime(nums[1], nums[0], 1))
            month_end = (month_start + datetime.timedelta(32)).replace(day=1)

    tasks_week = {}
    projects_week = {}
    tasks_month = {}
    projects_month = {}

    for time in TimeEntry.objects.all():
        duration = time.end_time - time.start_time
        task = Task.objects.get(id=time.task)

        if time.start_time > week_start and time.end_time < week_end:
            if task in tasks_week:
                tasks_week[task] += duration
            else:
                tasks_week[task] = duration

            if task.project in projects_week:
                projects_week[task.project] += duration
            else:
                projects_week[task.project] = duration
        elif time.start_time < week_start and time.end_time > week_start and time.end_time < week_end:
            if task in tasks_week:
                tasks_week[task] += time.end_time - week_start
            else:
                tasks_week[task] = time.end_time - week_start

            if task.project in projects_week:
                projects_week[task.project] += time.end_time - week_start
            else:
                projects_week[task.project] = time.end_time - week_start
        elif time.start_time > week_start and time.start_time < week_end and time.end_time > week_end:
            if task in tasks_week:
                tasks_week[task] += week_end - time.start_time
            else:
                tasks_week[task] = week_end - time.start_time

            if task.project in projects_week:
                projects_week[task.project] += week_end - time.start_time
            else:
                projects_week[task.project] = week_end - time.start_time
        elif time.start_time < week_start and time.end_time > week_end:
            if task in tasks_week:
                tasks_week[task] += week_end - week_start
            else:
                tasks_week[task] = week_end - week_start

            if task.project in projects_week:
                projects_week[task.project] += week_end - week_start
            else:
                projects_week[task.project] = week_end - week_start

        if time.start_time > month_start and time.end_time < month_end:
            if task in tasks_month:
                tasks_month[task] += duration
            else:
                tasks_month[task] = duration

            if task.project in projects_month:
                projects_month[task.project] += duration
            else:
                projects_month[task.project] = duration
        elif time.start_time < month_start and time.end_time > month_start and time.end_time < month_end:
            if task in tasks_month:
                tasks_month[task] += time.end_time - month_start
            else:
                tasks_month[task] = time.end_time - month_start

            if task.project in projects_month:
                projects_month[task.project] += time.end_time - month_start
            else:
                projects_month[task.project] = time.end_time - month_start
        elif time.start_time > month_start and time.start_time < month_end and time.end_time > month_end:
            if task in tasks_month:
                tasks_month[task] += month_end - time.start_time
            else:
                tasks_month[task] = month_end - time.start_time

            if task.project in projects_month:
                projects_month[task.project] += month_end - time.start_time
            else:
                projects_month[task.project] = month_end - time.start_time
        elif time.start_time < month_start and time.end_time > month_end:
            if task in tasks_month:
                tasks_month[task] += month_end - month_start
            else:
                tasks_month[task] = month_end - month_start

            if task.project in projects_month:
                projects_month[task.project] += month_end - month_start
            else:
                projects_month[task.project] = month_end - month_start

    return render(request, 'time_dashboard.html', {'tasks_week': tasks_week, 'tasks_month': tasks_month, 'projects_week': projects_week, 'projects_month': projects_month, 'week_start': week_start.strftime("%m/%d/%Y"), 'week_end': week_end.strftime("%m/%d/%Y"), 'month': month_start.strftime("%b %Y")})

def task_dashboard(request):
    global week_start, week_end, month_start, month_end, utc

    if request.method == 'POST': 
        if request.POST['action'] == 'week':
            nums = [int(x) for x in request.POST.get('date').split('/')]
            date = datetime.datetime(nums[2], nums[0], nums[1])
            week_start = utc.localize(date)
            week_end = week_start + datetime.timedelta(7)

        elif request.POST['action'] == 'month':
            nums = [int(x) for x in request.POST.get('month').split('/')]
            month_start = utc.localize(datetime.datetime(nums[1], nums[0], 1))
            month_end = (month_start + datetime.timedelta(32)).replace(day=1)

    tasks_week = {}
    tasks_month = {}
    tasks_week_count = {}
    tasks_month_count = {}
    tasks_week_avg = {}
    tasks_month_avg = {}
    
    for time in TimeEntry.objects.all():
            duration = time.end_time - time.start_time
            task = Task.objects.get(id=time.task)

            if time.start_time > week_start and time.end_time < week_end:
                if task in tasks_week:
                    tasks_week[task] += duration
                    tasks_week_count[task] += 1
                else:
                    tasks_week[task] = duration
                    tasks_week_count[task] = 1

            elif time.start_time < week_start and time.end_time > week_start and time.end_time < week_end:
                if task in tasks_week:
                    tasks_week[task] += time.end_time - week_start
                    tasks_week_count[task] += 1
                else:
                    tasks_week[task] = time.end_time - week_start
                    tasks_week_count[task] = 1

            elif time.start_time > week_start and time.start_time < week_end and time.end_time > week_end:
                if task in tasks_week:
                    tasks_week[task] += week_end - time.start_time
                    tasks_week_count[task] += 1
                else:
                    tasks_week[task] = week_end - time.start_time
                    tasks_week_count[task] = 1

            elif time.start_time < week_start and time.end_time > week_end:
                if task in tasks_week:
                    tasks_week[task] += week_end - week_start
                    tasks_week_count[task] += 1
                else:
                    tasks_week[task] = week_end - week_start
                    tasks_week_count[task] = 1

            if time.start_time > month_start and time.end_time < month_end:
                if task in tasks_month:
                    tasks_month[task] += duration
                    tasks_month_count[task] += 1
                else:
                    tasks_month[task] = duration
                    tasks_month_count[task] = 1

            elif time.start_time < month_start and time.end_time > month_start and time.end_time < month_end:
                if task in tasks_month:
                    tasks_month[task] += time.end_time - month_start
                    tasks_month_count[task] += 1
                else:
                    tasks_month[task] = time.end_time - month_start
                    tasks_month_count[task] = 1

            elif time.start_time > month_start and time.start_time < month_end and time.end_time > month_end:
                if task in tasks_month:
                    tasks_month[task] += month_end - time.start_time
                    tasks_month_count[task] += 1
                else:
                    tasks_month[task] = month_end - time.start_time
                    tasks_month_count[task] = 1

            elif time.start_time < month_start and time.end_time > month_end:
                if task in tasks_month:
                    tasks_month[task] += month_end - month_start
                    tasks_month_count[task] += 1
                else:
                    tasks_month[task] = month_end - month_start
                    tasks_month_count[task] = 1

    for task, time in tasks_week.items():
       tasks_week_avg[task] = datetime.timedelta(seconds=int(time.total_seconds() / tasks_week_count[task]))

    for task, time in tasks_month.items():
       tasks_month_avg[task] = datetime.timedelta(seconds=int(time.total_seconds() / tasks_month_count[task]))

    return render(request, 'task_dashboard.html', {'tasks_week_avg': tasks_week_avg, 'tasks_month_avg': tasks_month_avg, 'week_start': week_start.strftime("%m/%d/%Y"), 'week_end': week_end.strftime("%m/%d/%Y"), 'month': month_start.strftime("%b %Y")})