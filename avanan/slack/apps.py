from django.apps import AppConfig


class SlackConfig(AppConfig):
    name = 'avanan.slack'

    def ready(self):
        from avanan.slack.signals import handlers
        pass
