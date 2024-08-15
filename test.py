import re
from typing import Final


PATTERN: Final[str] = "(\d+)\/(\d+(s|m|h))+"

def retrieve_duration(duration: str):
    try:
        hits = re.search(PATTERN, duration)
        durations = re.search(PATTERN, duration)
        return hits, durations
    except re.error as e:
        print(e.msg)
    except AttributeError as e:
        print(e)
    return None, None
    


print(retrieve_duration("16m"))