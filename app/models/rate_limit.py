from typing import Optional
from sqlmodel import SQLModel


class CachedRateLimit(SQLModel):
    last_hit_time: Optional[float] = None
    count: Optional[int] = None   
