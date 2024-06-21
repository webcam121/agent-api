import json
from datetime import datetime

from celery import shared_task

from agent.apps.call_schedules.tasks import run_scheduled_call
from agent.apps.call_sessions.tasks import summarize_call_session
from agent.apps.eta_tasks.models import ETATask
from agent.apps.notifications.tasks import \
    send_abandoned_cart_notification_for_accounts_created_between_24_25_hrs_ago


@shared_task
def run_eta_tasks():
    now = datetime.now()
    tasks = ETATask.objects.filter(finished=False, run_at__lte=now)
    for task in tasks:
        try:
            task_kwargs = json.loads(task.task_kwargs)
        except Exception as e:  # Invalid task_kwargs
            print(e)
            continue

        if not task_kwargs:
            task_kwargs = {}

        if task.task_name == 'send_abandoned_cart_notification_for_accounts_created_between_24_25_hrs_ago':
            send_abandoned_cart_notification_for_accounts_created_between_24_25_hrs_ago.delay(**task_kwargs)
        elif task.task_name == 'run_scheduled_call':
            run_scheduled_call.delay(**task_kwargs)
        elif task.task_name == 'summarize_call_session':
            summarize_call_session.delay(**task_kwargs)
        else:
            continue

        task.finished = True
        task.save()
    return True
