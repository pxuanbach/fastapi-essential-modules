from datetime import datetime
from typing import Any, List, Literal, Optional, Union
from sqlmodel import SQLModel


class CronArgs(SQLModel):
    year: Optional[str] = "*"
    month: Optional[str] = "*"
    day: Optional[str] = "*" 
    week: Optional[str] = "*"
    day_of_week: Optional[str] = "*"
    hour: Optional[str] = "*"
    minute: Optional[str] = "*"
    second: Optional[str] = "5"


class IntervalArgs(SQLModel):
    seconds: Optional[int] = 10
    minutes: Optional[int] = None
    hours: Optional[int] = None
    days: Optional[int] = None
    weeks: Optional[int] = None


class DateArgs(SQLModel):
    args: List[Any] = []
    run_date: datetime = datetime.now()


class JobCreate(SQLModel):
    job_id: str
    from_file: bool = True
    type: Literal['cron', 'interval', 'date'] = 'cron'
    args: Optional[Union[DateArgs, IntervalArgs, CronArgs]] = None


class JobCreateDeleteResponse(SQLModel):
    scheduled: bool
    job_id: str
