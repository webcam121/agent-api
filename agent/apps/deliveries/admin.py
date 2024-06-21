from django.contrib import admin

from agent.apps.deliveries.models import Delivery


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'giver', 'receiver', 'pre_receiver', 'delivery_date', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'giver', 'receiver', 'pre_receiver')


admin.site.register(Delivery, DeliveryAdmin)
