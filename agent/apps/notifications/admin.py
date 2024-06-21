from django.contrib import admin

from agent.apps.notifications.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_type', 'created_at', 'user', 'metadata')
    search_fields = ['user__email', 'notification_type']
    readonly_fields = ('user',)


admin.site.register(Notification, NotificationAdmin)
