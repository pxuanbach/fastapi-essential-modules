from typing import Any
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.engine import create_engine
import logging

from app.core.config import settings
from app import models


async def call(
    *args: Any, 
    **kwds: Any,
) -> Any:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    session = SessionLocal()
    session.rollback()
    session.commit()

    try:
        import random
        num = random.randint(0, 19999)
        logging.info(f"get_random_user {num}")
        user = session.query(models.UserInDb).offset(num).first()
        logging.info(f"get_random_user {num} - User {user.id}, email {user.email}")
    except Exception as e:
        logging.error(f"get_random_user - {str(e)}")
    finally:
        session.close()
        engine.dispose()
