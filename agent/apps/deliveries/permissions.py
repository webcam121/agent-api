from rest_framework import permissions

from agent.apps.accounts.models import CustomUser, GiftGiver, GiftReceiver


class IsObjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        gift_giver = GiftGiver.objects.filter(user=request.user).first()
        gift_receiver = GiftReceiver.objects.filter(user=request.user).first()
        return obj.giver == gift_giver or obj.receiver == gift_receiver
