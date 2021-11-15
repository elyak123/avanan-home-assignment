import json
import logging

from django.conf import settings
from slack_bolt import App

from avanan.slack.utils import produce_sqs

logger = logging.getLogger(__name__)

app = App(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_APP_TOKEN,
    token_verification_enabled=False,
)


@app.event("message")
def handle_app_messages(logger, event, ack, say):
    logger.info(event)
    ack()
    if not event.get('bot_id'):
        produce_sqs(json.dumps(event))


@app.event("file_shared")
def handle_file_shared_events(body, logger):
    logger.info(body)
