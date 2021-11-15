import logging
import os

from . import datatypes

logger = logging.getLogger(__name__)


def build_config():
    return datatypes.Config(
        queue_name=os.environ['DJANGO_AWS_SQS_MAIN_QUEUE'],
        region=os.environ.get('DJANGO_AWS_SQS_MAIN_QUEUE_REGION', 'us-west-2'),
        AWS_ACCESS_KEY_ID=os.environ['DJANGO_AWS_ACCESS_KEY_ID'],
        AWS_SECRET_ACCESS_KEY=os.environ['DJANGO_AWS_SECRET_ACCESS_KEY'],
        db_host=os.environ['MYSQL_ROOT_HOST'],
        db_port=os.environ['MYSQL_PORT'],
        db_user=os.environ['MYSQL_USER'],
        db_password=os.environ['MYSQL_PASSWORD'],
        db_name=os.environ['MYSQL_DATABASE'],
        django_url=os.environ.get('DJANGO_URL', 'http://django:8000')
    )


def custom_exception_handler(loop, context):  # pragma: no cover
    loop.default_exception_handler(context)
    logger.error(f"Stopping event loop due to: {context}")
    loop.stop()
