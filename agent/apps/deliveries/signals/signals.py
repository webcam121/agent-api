from datetime import datetime

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from agent.apps.deliveries.models import Delivery
from agent.apps.deliveries.tasks import send_delivery_email_task
from agent.apps.deliveries.utils import generate_delivery_email_content
from agent.apps.notifications.models import Notification
from agent.services import zendesk
from agent.services.constants import DELIVERY_NOTIFICATION


@receiver(post_save, sender=Delivery)
def send_delivery_email(sender, instance, created, update_fields, **kwargs):
    # Only for updated event
    if not created and update_fields and 'receiver' in update_fields:
        # Only when the receiver field is set
        if instance.receiver_id is not None:
            if instance.delivery_date <= timezone.now().date():
                send_delivery_email_task.delay(instance.pk)
