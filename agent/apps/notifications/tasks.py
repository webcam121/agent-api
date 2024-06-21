from datetime import datetime, timedelta
from celery import shared_task
from django.conf import settings
from django.db.models import Count, Q
import pytz
from agent.apps.accounts.models import CustomUser, ExpiringAuthToken, GiftGiver, GiftReceiver, \
    DailyUpdate
from agent.apps.call_schedules.models import CallSchedule
from agent.apps.deliveries.utils import generate_reset_password_email_content, generate_welcome_email_content, \
    generate_abandoned_cart_email_content, generate_gift_sent_email_content, generate_story_shared_email_content, \
    generate_story_shared_text_content, generate_reminder_email_content, generate_reminder_email_to_receiver_content, \
    generate_schedule_reminder_email_to_giver_content, generate_schedule_reminder_email_to_receiver_content
from agent.apps.notifications.models import Notification, AbandonNotification, NewStorySharedNotification, \
    GiftReceivedNotification
from agent.services import zendesk
from agent.services.constants import PASSWORD_RESET_LINK_NOTIFICATION, WELCOME_EMAIL_NOTIFICATION, \
    ABANDONED_CART_EMAIL_1_NOTIFICATION, GIFT_SENT_EMAIL_NOTIFICATION, STORY_SHARED_EMAIL_NOTIFICATION, \
    SEND_REMINDER_EMAIL_NOTIFICATION, SEND_REMINDER_EMAIL_TO_RECEIVER_NOTIFICATION, GIFT_SENDING_EMAIL_NOTIFICATION, \
    SEND_SCHEDULE_REMINDER_EMAIL_TO_GIVER_NOTIFICATION, SEND_SCHEDULE_REMINDER_EMAIL_TO_RECEIVER_NOTIFICATION


@shared_task
def send_password_reset_link(user_id, url):
    user = CustomUser.objects.get(pk=user_id)

    if zendesk.ZendeskAPI.send_notification(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            subject="Reset your Agent password",
            html_body=generate_reset_password_email_content(user, url),
            tags=[PASSWORD_RESET_LINK_NOTIFICATION],
            status='solved',
            sms=False,
    ):
        notification = Notification(notification_type=PASSWORD_RESET_LINK_NOTIFICATION, user=user)
        notification.save()


@shared_task
def send_welcome_email_to_giver(user_id):
    user = CustomUser.objects.filter(id=user_id, unsubscribed=False).first()
    token = ExpiringAuthToken(
        key=ExpiringAuthToken.generate_key(), user=user, expire_at=datetime.now() + timedelta(days=7)
    )
    url = settings.FRONTEND_BASE_URL + "set-password"
    if user:
        if zendesk.ZendeskAPI.send_notification(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                subject="Welcome to Agent!",
                html_body=generate_welcome_email_content(user, url, token),
                tags=[WELCOME_EMAIL_NOTIFICATION],
                status='solved',
                sms=False,
        ):
            notification = Notification(notification_type=WELCOME_EMAIL_NOTIFICATION, user=user)
            notification.save()
            token.save()


@shared_task
def send_abandoned_cart_notification_for_accounts_created_between_24_25_hrs_ago():
    now = datetime.now()
    success_count = 0  # notification sent successully
    fail_count = 0  # notification sent fail
    # queued_count = 0

    givers = GiftGiver.objects.annotate(
        active_plan_count=Count('giver_plans', filter=Q(giver_plans__is_active=True)),
        notification_count=Count('abandon_notifications',
                                 filter=Q(abandon_notifications__notification_type=ABANDONED_CART_EMAIL_1_NOTIFICATION))
    ).filter(
        user__is_active=True,
        user__unsubscribed=False,
        notification_count=0,
        user__date_joined__gte=now - timedelta(hours=25),
        user__date_joined__lte=now - timedelta(hours=24),
        active_plan_count=0
    )

    sent_users = []
    for giver in givers:
        token = ExpiringAuthToken(
            key=ExpiringAuthToken.generate_key(), user=giver.user, expire_at=datetime.now() + timedelta(days=7)
        )
        link = f"{settings.FRONTEND_BASE_URL}landing/introduction?token={token.key}" if not giver.user.self_gift else f"{settings.FRONTEND_BASE_URL}self/introduction?token={token.key}"

        try:
            notification = AbandonNotification.objects.create(
                notification_type=ABANDONED_CART_EMAIL_1_NOTIFICATION, giver=giver
            )
            if zendesk.ZendeskAPI.send_notification(
                    first_name=giver.user.first_name,
                    last_name=giver.user.last_name,
                    email=giver.user.email,
                    subject="Ready to bring a daily smile to your loved ones?" if not giver.user.self_gift else "You're Almost There! Complete Your Sign-Up with Agent",
                    html_body=generate_abandoned_cart_email_content(giver.user, link),
                    tags=[ABANDONED_CART_EMAIL_1_NOTIFICATION],
                    status='solved',
                    sms=False,
            ):
                token.save()
                sent_users.append(giver.pd)
                success_count += 1  # count success notification
            else:
                notification.delete()
                fail_count += 1  # count fail notification
        except Exception as e:
            pass


@shared_task
def send_gift_sent_email_to_giver(giver_id, receiver_id):
    giver = GiftGiver.objects.filter(pk=giver_id, user__unsubscribed=False).first()
    receiver = GiftReceiver.objects.filter(pk=receiver_id).first()
    if giver and receiver and giver.user != receiver.user:
        if zendesk.ZendeskAPI.send_notification(
                first_name=giver.user.first_name,
                last_name=giver.user.last_name,
                email=giver.user.email,
                subject=f"{receiver.user.first_name} received your gift!",
                html_body=generate_gift_sent_email_content(giver, receiver),
                tags=[GIFT_SENT_EMAIL_NOTIFICATION],
                status='solved',
                sms=False,
        ):
            notification = Notification(notification_type=GIFT_SENT_EMAIL_NOTIFICATION, user=giver.user)
            notification.save()


@shared_task
def send_story_shared_email_to_giver(receiver_id, message):
    receiver = GiftReceiver.objects.filter(pk=receiver_id).first()

    today = datetime.now().astimezone(pytz.timezone("America/Los_Angeles")).date()
    formatted_date = today.strftime("%m/%d/%Y")
    print("str date=====>", formatted_date)


    if receiver:
        givers = receiver.gift_giver.filter(user__unsubscribed=False).all()
        for giver in givers:

            # Check if daily update flag for the giver receiver is True
            is_daily_update = DailyUpdate.objects.filter(gift_giver=giver, gift_receiver=receiver, is_daily_update=True).exists()
            if is_daily_update:
                token = ExpiringAuthToken(
                    key=ExpiringAuthToken.generate_key(), user=giver.user, expire_at=datetime.now() + timedelta(days=7)
                )
                if zendesk.ZendeskAPI.send_notification(
                        first_name=giver.user.first_name,
                        last_name=giver.user.last_name,
                        email=giver.user.email,
                        subject=f"Agent Update {formatted_date}",
                        html_body=generate_story_shared_email_content(giver, receiver, message),
                        tags=[STORY_SHARED_EMAIL_NOTIFICATION],
                        status='solved',
                        sms=False,
                        body=generate_story_shared_text_content(giver, receiver, message),
                ):
                    notification = NewStorySharedNotification(
                        notification_type=STORY_SHARED_EMAIL_NOTIFICATION,
                        user=giver.user,
                        receiver=receiver
                    )
                    notification.save()
                    token.save()


@shared_task
def send_reminder_email_to_giver(receiver_id):
    receiver = GiftReceiver.objects.filter(pk=receiver_id).first()
    if receiver:
        givers = receiver.gift_giver.filter(user__unsubscribed=False).all()

        for giver in givers:
            if giver:
                number = "855-245-8653"
                if zendesk.ZendeskAPI.send_notification(
                        first_name=giver.user.first_name,
                        last_name=giver.user.last_name,
                        email=giver.user.email,
                        subject=f"We couldn't reach {receiver.user.first_name}",
                        html_body=generate_reminder_email_content(giver, receiver, number),
                        tags=[SEND_REMINDER_EMAIL_NOTIFICATION],
                        status='solved',
                        sms=False,
                ):
                    notification = Notification(notification_type=SEND_REMINDER_EMAIL_NOTIFICATION, user=giver.user)
                    notification.save()


@shared_task
def send_reminder_email_to_receiver(receiver_id):
    receiver = GiftReceiver.objects.filter(pk=receiver_id, user__unsubscribed=False).first()
    if receiver:
        number = "855-245-8653"
        if zendesk.ZendeskAPI.send_notification(
                first_name=receiver.user.first_name,
                last_name=receiver.user.last_name,
                email=receiver.user.email,
                subject="Everything OK?",
                html_body=generate_reminder_email_to_receiver_content(receiver, number),
                tags=[SEND_REMINDER_EMAIL_TO_RECEIVER_NOTIFICATION],
                status='solved',
                sms=False,
        ):
            notification = Notification(notification_type=SEND_REMINDER_EMAIL_TO_RECEIVER_NOTIFICATION,
                                        user=receiver.user)
            notification.save()


@shared_task
def send_schedule_reminder_email_to_giver():
    now = datetime.now()
    gift_sending_email_notifications = GiftReceivedNotification.objects.filter(
        notification_type=GIFT_SENDING_EMAIL_NOTIFICATION,
        created_at__gte=now - timedelta(hours=25),
        created_at__lte=now - timedelta(hours=24),
    )

    for notification in gift_sending_email_notifications:
        receiver = notification.receiver
        if receiver:
            # check if the receiver scheduled recurring call
            scheduled_exists = CallSchedule.objects.filter(receiver=receiver, is_recurring=True).exists()
            if not scheduled_exists:
                # Check if the receiver has an active user plan
                latest_paid_user_plan = UserPlan.objects.filter(receiver=receiver, is_active=True).order_by('-created_at').first()
                if latest_paid_user_plan:
                    giver = latest_paid_user_plan.giver
                    if giver and giver.user.unsubscribed is False and giver.user != receiver.user:
                        if zendesk.ZendeskAPI.send_notification(
                                first_name=giver.user.first_name,
                                last_name=giver.user.last_name,
                                email=giver.user.email,
                                subject=f"Remind {receiver.user.first_name} to schedule a time",
                                html_body=generate_schedule_reminder_email_to_giver_content(giver, receiver),
                                tags=[SEND_SCHEDULE_REMINDER_EMAIL_TO_GIVER_NOTIFICATION],
                                status='solved',
                                sms=False,
                        ):
                            notification = Notification(notification_type=SEND_SCHEDULE_REMINDER_EMAIL_TO_GIVER_NOTIFICATION,
                                                        user=receiver.user)
                            notification.save()


@shared_task
def send_schedule_reminder_email_to_receiver():
    now = datetime.now()
    gift_sending_email_notifications = GiftReceivedNotification.objects.filter(
        notification_type=GIFT_SENDING_EMAIL_NOTIFICATION,
        created_at__gte=now - timedelta(hours=25),
        created_at__lte=now - timedelta(hours=24),
    )

    for notification in gift_sending_email_notifications:
        receiver = notification.receiver
        if receiver and receiver.user.unsubscribed is False:
            # check if the receiver scheduled recurring call
            scheduled_exists = CallSchedule.objects.filter(receiver=receiver, is_recurring=True).exists()
            if not scheduled_exists:
                # Check if the receiver has an active user plan
                latest_paid_user_plan = UserPlan.objects.filter(receiver=receiver, is_active=True).order_by(
                    '-created_at').first()
                if latest_paid_user_plan and latest_paid_user_plan.giver:
                    giver = latest_paid_user_plan.giver
                    token = ExpiringAuthToken(
                        key=ExpiringAuthToken.generate_key(), user=receiver.user,
                        expire_at=datetime.now() + timedelta(days=7)
                    )
                    link = f"{settings.FRONTEND_BASE_URL}schedule-time?token={token.key}"
                    if zendesk.ZendeskAPI.send_notification(
                            first_name=receiver.user.first_name,
                            last_name=receiver.user.last_name,
                            email=receiver.user.email,
                            subject="Reminder: Schedule your Agent call",
                            html_body=generate_schedule_reminder_email_to_receiver_content(giver, receiver, link),
                            tags=[SEND_SCHEDULE_REMINDER_EMAIL_TO_RECEIVER_NOTIFICATION],
                            status='solved',
                            sms=False,
                    ):
                        notification = Notification(
                            notification_type=SEND_SCHEDULE_REMINDER_EMAIL_TO_RECEIVER_NOTIFICATION,
                            user=receiver.user)
                        notification.save()


@shared_task
def send_free_trial_ended_email_to_user(giver_id, receiver_id):
    print(giver_id, receiver_id)

