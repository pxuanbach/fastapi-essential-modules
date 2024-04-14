from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import UserInDb
from app.utils import generate_random_string


async def bulk_insert(db: AsyncSession, n=1000):
    for i in range(n):
        user = UserInDb.create(
            email=generate_random_string() + "@" + generate_random_string(),
            hashed_password=generate_random_string(),
            full_name=generate_random_string()
        )
        db.add(user)
        await db.flush()

    return await db.commit()


async def get_pagination(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = (
        select(UserInDb)
        .offset(skip)
        .limit(limit)
    )

    data = (await db.execute(query)).scalars().all()
    return data