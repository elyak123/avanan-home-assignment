import asyncio
import contextlib
import json
import logging
import re
import time

import boto3
import requests
import MySQLdb

from .datatypes import Config

logger = logging.getLogger(__name__)


class ProcessManager:

    def __init__(
        self,
        config: Config,
        exit_stack: contextlib.AsyncExitStack,
    ):
        self.config = config
        self.loop = asyncio.get_event_loop()
        self._queue_db: asyncio.Queue = asyncio.Queue()
        self._queue_django: asyncio.Queue = asyncio.Queue()
        self.exit_stack = exit_stack

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.warning("exit from context manager.")
        pass

    async def run(self):  # pragma: no cover
        await self.start()

    async def start(self):
        asyncio.ensure_future(self.main(), loop=self.loop)

    async def notify_django(self, payload):
        logger.info(str(payload))
        url = self.config.django_url + "/slack/delete-message/"
        try:
            req = requests.post(url, json=payload, auth=('javier', 'somesecret'))
        except requests.exceptions.ConnectionError:
            time.sleep(30)
            req = requests.post(url, json=payload)
        try:
            response = req.json()
        except json.decoder.JSONDecodeError:
            response = req.text
        logger.warning(str(response))

    async def get_boto_client(self):
        if not hasattr(self, 'client'):
            session = boto3.Session(
                aws_access_key_id=self.config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.config.AWS_SECRET_ACCESS_KEY,
            )
            self.client = session.resource("sqs", region_name=self.config.region)
            return self.client
        return self.client

    async def get_aws_queue(self):
        await self.get_boto_client()
        return self.client.get_queue_by_name(QueueName=self.config.queue_name)

    async def check_message(self, event):
        select_command = "SELECT * FROM dpl_pattern"
        db = MySQLdb.connect(
            host=self.config.db_host,
            user=self.config.db_user,
            passwd=self.config.db_password,
            db=self.config.db_name
        )
        cur = db.cursor()
        cur.execute(select_command)
        results = cur.fetchall()
        await self.check_regex_match(event, results)

    async def execute_sql(self, command, commit=True):
        db = MySQLdb.connect(
            host=self.config.db_host,
            user=self.config.db_user,
            passwd=self.config.db_password,
            db=self.config.db_name
        )
        cur = db.cursor()
        logger.warning(command)
        cur.execute(command)
        if commit:
            db.commit()
        return cur.fetchall()

    async def check_regex_match(self, event, results):
        notify_django = False
        for line in results:
            pattern = re.compile(line[3])
            leak = False
            insert_command = f"""
                INSERT INTO dpl_leak (message, channel, pattern_id) VALUES ('{event.get('text')}', '{event['channel']}', '{line[0]}');
            """
            if event.get("text") and pattern.match(event.get("text")):
                leak = True
                notify_django = True
            elif event.get("files"):
                if event["files"].get("preview") and pattern.match(event["files"]["preview"]):
                    leak = True
                    notify_django = True
                elif event["files"].get("name") and pattern.match(event["files"]["name"]):
                    leak = True
                    notify_django = True
            if leak:
                await self.execute_sql(insert_command)
        if notify_django:
            await self.notify_django({"timestamp": event["ts"], "channel": event["channel"]})

    async def _get_messages(self):
        """Read and pop messages from SQS queue
        """
        queue = await self.get_aws_queue()
        for message in queue.receive_messages():
            message_dict = json.loads(message.body)
            logger.warning("despues de serializacion")
            logger.warning(f"mensaje... \n{str(message_dict)}")
            await self.check_message(message_dict)
            logger.warning("no more messages...")
            message.delete()

    async def main(self):
        logger.warning("Initializing main loop....")
        while True:
            await self._get_messages()
