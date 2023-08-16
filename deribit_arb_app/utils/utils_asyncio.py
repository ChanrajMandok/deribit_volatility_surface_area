import asyncio
from logging import Logger
from typing import Awaitable

background_tasks = set()

def asyncio_create_task_log_exception(awaitable: Awaitable, logger: Logger,
                                      origin: str = "") -> asyncio.Task:
    
    async def _log_exception(awaitable):
        try:
            return await awaitable
        except Exception as e:
            if origin:
                # logger.info(f"{origin}: {str(e)}")
                pass
            else:
                # logger.info(f"no origin: {str(e)}")
                pass
    task = asyncio.create_task(_log_exception(awaitable), name=origin)
    
    # Add task to the set. This creates a strong reference.
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    
    return task

def loop_create_task_log_exception(loop: any, awaitable: Awaitable,
                                   logger: Logger, origin: str = "") -> asyncio.Task:
    
    async def _log_exception(awaitable):
        try:
            return await awaitable
        except Exception as e:      
            if origin:
                pass
            else:
                pass
                # logger.info(f"no origin: {str(e)}")
            if "no close frame received or sent" in str(e):
                raise Exception(str(e))
          
    task = loop.create_task(_log_exception(awaitable), name=origin)
    
    # Add task to the set. This creates a strong reference.
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    
    return task

def loop_run_forever_log_exception(loop: asyncio.AbstractEventLoop, awaitable: Awaitable,
                                   logger: Logger, origin: str = "") -> None:

    async def _log_exception(awaitable):
        try:
            return await awaitable
        except Exception as e:
            logger.error(f"{origin}: Unexpected exception: {str(e)}")
            if "no close frame received or sent" in str(e):
                raise Exception(str(e))
            return None

    # Create the task with your logging wrapper
    loop.create_task(_log_exception(awaitable), name=origin)

    # Run the loop forever
    loop.run_forever()

def loop_run_until_complete_log_exception(loop: asyncio.AbstractEventLoop, awaitable: Awaitable,
                                          logger: Logger, origin: str = "") -> None:

    async def _log_exception(awaitable):
        try:
            return await awaitable
        except Exception as e:
            logger.error(f"{origin}: Unexpected exception: {str(e)}")
            if "no close frame received or sent" in str(e):
                raise Exception(str(e))
            return None

    # Create the task with your logging wrapper
    task = loop.create_task(_log_exception(awaitable), name=origin)

    # Run the loop until the task completes
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