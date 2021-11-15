import logging

from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from avanan.slack.models import SQSQueue


logger = logging.getLogger(__name__)


def get_slack_webclient():
    return WebClient(token=settings.SLACK_USER_TOKEN)


def produce_sqs(message):
    queue_instance, created = SQSQueue.get_default_queue()
    queue = queue_instance.get_aws_queue()
    response = queue.send_message(MessageBody=message)
    return response


def delete_message(timestamp, channel):
    try:
        client = get_slack_webclient()
        response = client.chat_delete(
            channel=channel,
            ts=timestamp)
        logger.info(response)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        return e.response['error']
