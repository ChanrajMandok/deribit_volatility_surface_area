import asyncio
from logging import Logger
from typing import Awaitable

background_tasks = set()

def asyncio_create_task_log_exception(awaitable: Awaitable, logger: Logger, origin: str = "") -> asyncio.Task:
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
    task = asyncio.create_task(_log_exception(awaitable))
    
    # Add task to the set. This creates a strong reference.
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    
    return task

def loop_create_task_log_exception(loop: any, awaitable: Awaitable, logger: Logger, origin: str = "") -> asyncio.Task:
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
          
    task = loop.create_task(_log_exception(awaitable))
    
    # Add task to the set. This creates a strong reference.
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    
    return task

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()