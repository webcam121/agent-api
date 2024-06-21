from django.apps import AppConfig


class CallSessionsConfig(AppConfig):
    name = 'agent.apps.call_sessions'

    def ready(self):
        from .signals import call_sessions # noqa