from django.db import models

from agent.apps.accounts.models import CustomUser, GiftGiver, GiftReceiver, Prereceiver


class Delivery(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    giver = models.ForeignKey(GiftGiver, on_delete=models.CASCADE, related_name='delivery', blank=False, null=False)
    receiver = models.ForeignKey(GiftReceiver, on_delete=models.CASCADE, related_name='receiver_delivery', blank=True,
                                 null=True, default=None)
    pre_receiver = models.ForeignKey(Prereceiver, on_delete=models.CASCADE, related_name='pre_receiver_delivery',
                                     blank=True, null=True, default=None)
    delivery_date = models.DateField(blank=False, null=False)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
