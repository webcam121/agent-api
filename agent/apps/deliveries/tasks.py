from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from agent.apps.accounts.models import ExpiringAuthToken, GiftGiver, GiftReceiver
from agent.apps.deliveries.models import Delivery
from agent.apps.deliveries.utils import generate_delivery_email_content, \
     generate_delivery_email_content_for_themselves
from agent.apps.notifications.models import Notification, GiftReceivedNotification
from agent.apps.notifications.tasks import send_gift_sent_email_to_giver
from agent.services import zendesk
from agent.services.constants import PASSWORD_RESET_LINK_NOTIFICATION, DELIVERY_NOTIFICATION, \
    GIFT_SENDING_EMAIL_NOTIFICATION


@shared_task
def send_delivery_email_task(delivery_id=None):
    today = timezone.now().date()
    if delivery_id:
        delivery = Delivery.objects.filter(pk=delivery_id).first()
        send_single_delivery_email_task(delivery)
    else:
        # only get the deliveries which have receiver: it means giver paid for receiver
        deliveries_today = Delivery.objects.filter(delivery_date=today, receiver__isnull=False)
        for delivery in deliveries_today:
            send_single_delivery_email_task(delivery)


@shared_task
def send_single_delivery_email_task(delivery):
    receiver = delivery.receiver
    giver = delivery.giver
    token = ExpiringAuthToken(
        key=ExpiringAuthToken.generate_key(), user=receiver.user, expire_at=datetime.now() + timedelta(days=7)
    )
    link = f"{settings.FRONTEND_BASE_URL}schedule-time?token={token}"
    if receiver and giver and receiver.user.unsubscribed is False:
        # if receiver.user == giver.user:
        #     if zendesk.ZendeskAPI.send_notification(
        #             first_name=receiver.user.first_name,
        #             last_name=receiver.user.last_name,
        #             email=receiver.user.email,
        #             subject="Schedule a time for your weekly call with Agent",
        #             html_body=generate_delivery_email_content_for_themselves(giver, receiver, link, delivery.message),
        #             tags=[GIFT_SENDING_EMAIL_NOTIFICATION],
        #             status='solved',
        #             sms=False,
        #     ):
        #         notification = Notification(notification_type=GIFT_SENDING_EMAIL_NOTIFICATION, user=receiver.user)
        #         notification.save()
        #         token.save()
        #         send_gift_sent_email_to_giver.delay(giver.pk, receiver.pk)
        # else:
        if receiver.user != giver.user:
            if zendesk.ZendeskAPI.send_notification(
                    first_name=receiver.user.first_name,
                    last_name=receiver.user.last_name,
                    email=receiver.user.email,
                    subject=f"{giver.user.first_name} {giver.user.last_name} has a gift for you at Agent!",
                    html_body=generate_delivery_email_content(giver, receiver, link),
                    tags=[GIFT_SENDING_EMAIL_NOTIFICATION],
                    status='solved',
                    sms=False,
            ):
                notification = Notification(notification_type=GIFT_SENDING_EMAIL_NOTIFICATION, user=receiver.user)
                notification.save()
                token.save()
                send_gift_sent_email_to_giver.delay(giver.pk, receiver.pk)


@shared_task()
def send_gift_received_email_to_receiver_task(giver_id, receiver_id):
    giver = GiftGiver.objects.filter(pk=giver_id).first()
    receiver = GiftReceiver.objects.filter(pk=receiver_id).first()

    notification_exists = GiftReceivedNotification.objects.filter(giver=giver, receiver=receiver).exists()

    token = ExpiringAuthToken(
        key=ExpiringAuthToken.generate_key(), user=receiver.user, expire_at=datetime.now() + timedelta(days=7)
    )
    link = f"{settings.FRONTEND_BASE_URL}schedule-time?token={token}"
    if receiver and giver and receiver.user.unsubscribed is False and not notification_exists:
        if receiver.user != giver.user:
            if zendesk.ZendeskAPI.send_notification(
                    first_name=receiver.user.first_name,
                    last_name=receiver.user.last_name,
                    email=receiver.user.email,
                    subject=f"{giver.user.first_name} {giver.user.last_name} has a gift for you at Agent!",
                    html_body=generate_delivery_email_content(giver, receiver, link),
                    tags=[GIFT_SENDING_EMAIL_NOTIFICATION],
                    status='solved',
                    sms=False,
            ):
                notification = GiftReceivedNotification(notification_type=GIFT_SENDING_EMAIL_NOTIFICATION, giver=giver, receiver=receiver)
                notification.save()
                token.save()
                send_gift_sent_email_to_giver.delay(giver.pk, receiver.pk)
