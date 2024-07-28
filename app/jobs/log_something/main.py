from typing import Any
import logging


async def call(
    *args: Any, 
    **kwds: Any,
) -> Any:
    logging.info("log_something")