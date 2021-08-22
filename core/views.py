from django.shortcuts import render
from django.contrib import messages

from .forms import SendEmailForm
from .tasks import send_email_task


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