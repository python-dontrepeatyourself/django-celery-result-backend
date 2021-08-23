from celery.result import AsyncResult

from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse

from .forms import SendEmailForm
from .tasks import send_email_task, loop


def index(request):
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():            
            email = form.cleaned_data['email']
            send_email_task.delay(email)
            messages.success(request, 'Sending email to {}'.format(email))
            return render(request, 'index.html', {'form': form})
            

    form = SendEmailForm()
    return render(request, 'index.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def run_long_task(request):
    if request.method == 'POST':
        l = request.POST.get('l')
        task = loop.delay(l)
        return JsonResponse({"task_id": task.id}, status=202)
    
def task_status(request, task_id):
    task = AsyncResult(task_id)
    if task.state == 'FAILURE' or task.state == 'PENDING':
        response = {
            'task_id': task_id,
            'state': task.state,
            'progression': "None",
            'info': str(task.info)
        }
        return JsonResponse(response, status=200)
    current = task.info.get('current', 0)
    total = task.info.get('total', 1)
    progression = (int(current) / int(total)) * 100 # to display a percentage of progress of the task
    response = {
        'task_id': task_id,
        'state': task.state,
        'progression': progression,
        'info': "None"
    }
    return JsonResponse(response, status=200)