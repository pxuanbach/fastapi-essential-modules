import re
from typing import Final


PATTERN: Final[str] = "(\d+)\/((\d+)(s|m|h))+"

def retrieve_duration(duration: str):
    try:
        hits = re.search(PATTERN, duration).group(1)
        durations = re.search(PATTERN, duration).group(3)
        period = re.search(PATTERN, duration).group(4)
        return hits, durations, period
    except re.error as e:
        print(e.msg)
    except AttributeError as e:
        print(e)
    return None, None
    


print(int("m"))