from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from app.core.config import settings


jobstores = {
    'default': SQLAlchemyJobStore(url=settings.JOB_DATABASE_URI)
}
scheduler = AsyncIOScheduler(jobstores=jobstores)
