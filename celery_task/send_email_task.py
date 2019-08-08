from celery_task.celery import app
from HHHmusicapi.utils.smtp import QqEmail
send_email = QqEmail()

@app.task
def send(recv, content):
    send_email.send(recv, content)
    return 'ok'
