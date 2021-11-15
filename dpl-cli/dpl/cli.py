import asyncio
import contextlib
import logging
import logging.config
import signal
import traceback

import click

from . import manager, datatypes, util

logger = logging.getLogger(__name__)


@click.command()
def main():
    """Console script for Data Loss Prevention Tool."""
    try:
        # Build Config
        config: datatypes.Config = util.build_config()

        logger.warning("DPL Tool: Launching")

        asyncio.run(run(config))
    except asyncio.CancelledError:  # pragma: no cover
        logger.error("Received asyncio.CancelledError")
    except Exception:  # pragma: no cover
        logger.error(f"{traceback.format_exc()}")
    finally:
        logger.info("DPL Tool: Shutting Down")


async def run(config: datatypes.Config):
    # Configure Exception Handler for the Event Loop
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(util.custom_exception_handler)

    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s, loop)))

    async with contextlib.AsyncExitStack() as exit_stack:
        dpl_controller = await exit_stack.enter_async_context(
            manager.ProcessManager(config, exit_stack)
        )
        await dpl_controller.run()


async def shutdown(signal, loop):  # pragma: no cover
    logging.warning(f"Received exit signal {signal.name}")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    for task in tasks:
        task.cancel()

    logging.warning("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
