from django.core.management.base import BaseCommand

from avanan.slack.models import SQSQueue


class Command(BaseCommand):
    def handle(self, *args, **options):
        obj, created = SQSQueue.get_default_queue()
        if created:
            self.stdout.write(self.style.SUCCESS('Main queue created successfully.'))
        self.stdout.write(
            self.style.SUCCESS(f"Main queue's url is: {str(obj.get_aws_queue().url)}")
        )
