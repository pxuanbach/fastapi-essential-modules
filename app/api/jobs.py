import importlib
import logging
from os import path
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks, status
from apscheduler.jobstores.base import ConflictingIdError

from app.utils import read_file_line_by_line
from app.core.scheduler import scheduler
from app.core.config import settings
from app.deps.db import get_async_session
from app.models.job import JobCreate, JobCreateDeleteResponse, CronArgs, IntervalArgs, DateArgs


router = APIRouter(prefix="/jobs")


@router.get(
    "",
)
async def get_scheduled_jobs():
    schedules = []
    for job in scheduler.get_jobs():
        schedules.append({
            "job_id": str(job.id), 
            "run_frequency": str(job.trigger), 
            "next_run": str(job.next_run_time)
        })
    return {
        "total": len(schedules),
        "jobs": schedules
    }


@router.post(
    "",
    response_model=JobCreateDeleteResponse
)
async def add_job_to_scheduler(
    obj_in: JobCreate,
) -> JobCreateDeleteResponse:
    # Find job folder
    job_folder = path.join("app", settings.JOB_DIR, obj_in.job_id)
    if not path.exists(job_folder):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job folder not found."
        )
    
    _timers = obj_in.args
    if obj_in.from_file:
        _timers = {}
        _sched_path = path.join(job_folder, ".schedule")
        if not path.exists(_sched_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Schedule file not found"
            )
    
        sched = read_file_line_by_line(_sched_path)
        for i in range(len(sched)):
            if i == 0 or str(sched[i]).startswith('#') or sched[i] == '' or sched[i] is None:
                continue 
            _interval_timer = str(sched[i]).split("=")
            _timers.update({
                _interval_timer[0]: _interval_timer[1]
            })
    if obj_in.type == "cron":
        _timers = CronArgs.model_validate(_timers)
    elif obj_in.type == "interval":
        _timers = IntervalArgs.model_validate(_timers)
    elif obj_in.type == "date":
        _timers = DateArgs.model_validate(_timers)

    _job_model = importlib.import_module(f"app.jobs.{obj_in.job_id}.main")
    try:
        job = scheduler.add_job(
            _job_model.call, 
            obj_in.type, 
            id=obj_in.job_id,
            **_timers.model_dump(exclude_none=True)
        )
    except ConflictingIdError:
        logging.warning(f"Job {obj_in.job_id} already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Job already exists"
        )
    except Exception as e:
        logging.error(f"Add job {obj_in.job_id} - {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred"
        )
    return JobCreateDeleteResponse(
        scheduled = True,
        job_id = job.id
    )


@router.delete(
    "/{job_id}",
    response_model=JobCreateDeleteResponse
)
async def remove_job_from_scheduler(
    job_id: str,
) -> JobCreateDeleteResponse:
    """
    Remove a Job from a Schedule
    """
    try:
        scheduler.remove_job(job_id)
    except Exception as e:
        logging.error(f"Delete job {job_id} - {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job deleted failed"
        )
    return JobCreateDeleteResponse(
        scheduled = False,
        job_id = job_id
    )
