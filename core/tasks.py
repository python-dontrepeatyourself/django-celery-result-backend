import time
from celery import shared_task
from mysite.celery import app

from django.core.mail import send_mail


@shared_task
def add(x, y):
    return x + y

@shared_task
def send_email_task(email):
    "background task to send an email asynchronously"
    subject = 'Helo from Celery'
    message = 'This is a test email sent asynchronously with Celery.'
    
    time.sleep(5)
    return send_mail(
        subject,
        message,
        'alfabravo318@gmail.com', # from
        [email], # to
        fail_silently=False
    )
    
@app.task(bind=True)
def loop(self, l):
    "simulate a long-running task like export of data or generateing a report"
    for i in range(int(l)):
        time.sleep(1)
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': l})
    print('Task completed')
    return {'current': 100, 'total': 100, }