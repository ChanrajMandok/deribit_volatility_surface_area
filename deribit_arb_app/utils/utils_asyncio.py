import asyncio

from logging import Logger
from typing import Awaitable

background_tasks = set()

async def _log_exception(awaitable: Awaitable, logger: Logger, origin: str = ""):
    try:
        return await awaitable
    except Exception as e:
        msg = f"{origin}: Unexpected exception: {str(e)}" if origin else f"Unexpected exception: {str(e)}"
        
        # Log the exception
        logger.error(msg)
        
        # Propagate specific critical exceptions
        if "no close frame received or sent" in str(e):
            logger.error(str(e))
        
        return None

def asyncio_create_task_log_exception(awaitable: Awaitable, logger: Logger,
                                      origin: str = "") -> asyncio.Task:
    
    task = asyncio.create_task(_log_exception(awaitable, logger, origin), name=origin)
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    return task

def loop_create_task_log_exception(loop: any, awaitable: Awaitable,
                                   logger: Logger, origin: str = "") -> asyncio.Task:

    task = loop.create_task(_log_exception(awaitable, logger, origin), name=origin)
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    return task

def loop_run_forever_log_exception(loop: asyncio.AbstractEventLoop, awaitable: Awaitable,
                                   logger: Logger, origin: str = "") -> None:

    loop.create_task(_log_exception(awaitable, logger, origin), name=origin)
    loop.run_forever()

def loop_run_until_complete_log_exception(loop: asyncio.AbstractEventLoop, awaitable: Awaitable,
                                          logger: Logger, origin: str = "") -> None:

    task = loop.create_task(_log_exception(awaitable, logger, origin), name=origin)
    loop.run_until_complete(task)

    # Wait for all other pending tasks to complete as well
    pending = asyncio.all_tasks(loop=loop)
    loop.run_until_complete(asyncio.gather(*pending))

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()
