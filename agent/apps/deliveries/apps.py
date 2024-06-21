from django.apps import AppConfig


class DeliveriesConfig(AppConfig):
    name = 'agent.apps.deliveries'

    def ready(self):
        from .signals import signals # noqa