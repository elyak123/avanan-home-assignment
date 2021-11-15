from django.db.models.signals import post_save
from django.dispatch import receiver

from avanan.slack.models import SQSQueue


@receiver(post_save, sender=SQSQueue)
def create_SQSQueue(sender, instance, created, **kwargs):
    if created:
        instance.create_aws_queue()
