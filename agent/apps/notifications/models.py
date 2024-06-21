from django.db import models

from agent.apps.accounts.models import CustomUser, GiftGiver, GiftReceiver, Prereceiver


class Notification(models.Model):
    notification_type = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='notifications')
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'notifications'
        indexes = [models.Index(fields=['notification_type'])]


class AbandonNotification(models.Model):
    notification_type = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    giver = models.ForeignKey(GiftGiver, on_delete=models.CASCADE, null=False, related_name='abandon_notifications')
    pre_receiver = models.ForeignKey(Prereceiver, on_delete=models.CASCADE, blank=True, null=True, related_name='prereceiver_abandon_notifications')
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'abandon_notifications'
        constraints = [
            models.UniqueConstraint(fields=['giver_id', 'notification_type', 'pre_receiver'], name='unique_user_notification')
        ]


class GiftReceivedNotification(models.Model):
    notification_type = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    giver = models.ForeignKey(GiftGiver, on_delete=models.CASCADE, null=False, related_name='gift_received_notifications')
    receiver = models.ForeignKey(GiftReceiver, on_delete=models.CASCADE, null=False, related_name='receiver_gift_received_notifications')
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'gift_received_notifications'
        indexes = [models.Index(fields=['notification_type'])]


class NewStorySharedNotification(models.Model):
    notification_type = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='new_story_notifications')
    receiver = models.ForeignKey(GiftReceiver, on_delete=models.CASCADE, null=False, related_name='receiver_new_story_notifications')
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'new_story_notifications'
        indexes = [models.Index(fields=['notification_type'])]
