from typing import Any
import logging


async def call(
    *args: Any, 
    **kwds: Any,
) -> Any:
    from pprint import pprint
    pprint(args[0])
    logging.info("log_something")