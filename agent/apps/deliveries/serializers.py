from rest_framework import serializers

from agent.apps.deliveries.models import Delivery


class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = ('pk', 'created_at', 'updated_at', 'giver', 'receiver', 'pre_receiver', 'delivery_date', 'message')
        extra_kwargs = {
            'giver': {'read_only': True},
            'receiver': {'read_only': True},
            'pre_receiver': {'read_only': True}
        }
