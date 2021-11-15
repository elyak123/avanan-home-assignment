import boto3
from django.db import models
from django.conf import settings


class SQSQueue(models.Model):
    name = models.CharField(max_length=20, unique=True)
    region = models.CharField(max_length=20, default="us-west-2")
    delay_seconds = models.IntegerField(default=0)
    visibility_timeout = models.IntegerField(default=60)

    class Meta:
        verbose_name = "SQSQueue"
        verbose_name_plural = "SQSQueues"

    def __str__(self):
        return self.queue_name

    def get_boto_client(self):
        if not hasattr(self, 'client'):
            session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            self.client = session.resource("sqs", region_name=self.region)
            return self.client
        return self.client

    def get_aws_queue(self):
        self.get_boto_client()
        return self.client.get_queue_by_name(QueueName=self.name)

    def create_aws_queue(self):
        self.get_boto_client()
        self.client.create_queue(
            QueueName=self.name,
            Attributes={
                "DelaySeconds": str(self.delay_seconds),
                "VisibilityTimeout": str(self.visibility_timeout),
            }
        )

    @staticmethod
    def get_default_queue():
        return SQSQueue.objects.get_or_create(
            name=settings.DJANGO_AWS_SQS_MAIN_QUEUE,
            region=settings.DJANGO_AWS_SQS_MAIN_QUEUE_REGION
        )
