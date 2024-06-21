from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from agent.apps.accounts.models import CustomUser, GiftGiver, GiftReceiver, Prereceiver
from agent.apps.accounts.permissions import IsGiftGiver
from agent.apps.deliveries.models import Delivery
from agent.apps.deliveries.permissions import IsObjectOwner
from agent.apps.deliveries.serializers import DeliverySerializer
from agent.apps.deliveries.utils import generate_delivery_email_content
from agent.apps.notifications.models import Notification
from agent.services import zendesk
from agent.services.constants import DELIVERY_NOTIFICATION


class ListDeliveryView(generics.ListCreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated, IsGiftGiver]

    def get_queryset(self):
        giver_user = self.request.user
        receiver_id = self.kwargs.get('receiver_id')
        gift_giver = get_object_or_404(GiftGiver, user=giver_user)
        gift_receiver = get_object_or_404(GiftReceiver, pk=receiver_id)
        if not gift_giver.gift_receivers.filter(user=gift_receiver.user).exists():
            raise PermissionDenied("You don't have permission to do action")
        return Delivery.objects.filter(
            giver__user=giver_user,
            receiver__user__id=receiver_id)

    def perform_create(self, serializer):
        gift_giver = get_object_or_404(GiftGiver, user=self.request.user)
        gift_receiver_id = self.kwargs['receiver_id']
        gift_receiver = get_object_or_404(GiftReceiver, pk=gift_receiver_id)
        if not gift_giver.gift_receivers.filter(user=gift_receiver.user).exists():
            raise PermissionDenied("You don't have permission to do action")
        serializer.save(giver=gift_giver, receiver=gift_receiver)


class ListPreReceiverDeliveryView(generics.ListCreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated, IsGiftGiver]

    def get_queryset(self):
        giver_user = self.request.user
        giver = get_object_or_404(GiftGiver, user=giver_user)
        pre_receiver_id = self.kwargs.get('pre_receiver_id')
        pre_receiver = get_object_or_404(Prereceiver, pk=pre_receiver_id)
        if pre_receiver.giver != giver:
            raise PermissionDenied("You don't have permission to do action")
        return Delivery.objects.filter(
            giver__user=giver_user,
            pre_receiver_id=pre_receiver_id)

    def perform_create(self, serializer):
        gift_giver_user = CustomUser.objects.get(id=self.request.user.id)
        gift_giver = GiftGiver.objects.get(user=gift_giver_user)
        pre_receiver_id = self.kwargs['pre_receiver_id']
        pre_receiver = get_object_or_404(Prereceiver, pk=pre_receiver_id)
        if pre_receiver.giver != gift_giver:
            raise PermissionDenied("You don't have permission to do action")
        serializer.save(giver=gift_giver, pre_receiver=pre_receiver)


class DetailDeliveryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]


class TestDeliveryView(APIView):

    def get(self, request, *args, **kwargs):
        # today = timezone.now().date()
        # deliveries_today = Delivery.objects.filter(delivery_date=today)
        #
        # for delivery in deliveries_today:
        #     subject = 'Delivery Notification'
        #     message = f'Your delivery is scheduled for {delivery.delivery_date}.'
        #     sender_email = 'your_sender_email@example.com'
        #     recipient_email = delivery.receiver.user.email
        #     # send_mail(subject, message, sender_email, [recipient_email])
        #     print(subject, message, sender_email, recipient_email)
        user = CustomUser.objects.get(email='kai@meetbeagle.com')
        subject = 'Delivery Notification'
        if zendesk.ZendeskAPI.send_notification(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                subject=subject,
                html_body=generate_delivery_email_content(user),
                tags=[DELIVERY_NOTIFICATION],
                status='solved',
                sms=False,
        ):
            notification = Notification(notification_type=DELIVERY_NOTIFICATION, user=user)
            notification.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RetrieveLatestPreReceiverDeliveryView(APIView):
    permission_classes = [IsAuthenticated, IsGiftGiver]
    serializer_class = DeliverySerializer

    def get(self, request, *args, **kwargs):
        giver_user = self.request.user
        gift_giver = get_object_or_404(GiftGiver, user=giver_user)
        pre_receiver_id = kwargs.get('pre_receiver_id')
        pre_receiver = get_object_or_404(Prereceiver, pk=pre_receiver_id)
        if pre_receiver.giver != gift_giver:
            return Response({"message": "The Giver didn't register this Pre-Receiver"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            latest_delivery = Delivery.objects.filter(giver=gift_giver, pre_receiver=pre_receiver).order_by('-created_at').first()
            if latest_delivery:
                serializer = self.serializer_class(latest_delivery)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No deliveries found for the gift giver and pre-receiver'},
                                status=status.HTTP_404_NOT_FOUND)
