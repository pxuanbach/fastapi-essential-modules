import random
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.attr import AttrInDb
from app.utils import generate_random_string


async def bulk_insert(db: AsyncSession, n=1000):
    attr_head = [
        "Like", "Play", "Help", "Work", "Rest", "Relax", "Listen", 
        "Choose", "Read", "Lorem sum", "Become", "Learn", "Fly"
    ]
    attr_tail = [
        "Book", "Movie", "Video Game", "Music", "Dog", "Shower", 
        "Learning", "Remote", "illora", "Docter", "Docker", "K8S",
        "Youtube", "Python", "JavaScript", "WebRTC"
    ]

    for i in range(n):
        attr = AttrInDb.create(
            title=attr_head[random.randrange(0, 8)] + " " + attr_tail[random.randrange(0, 7)]
        )
        db.add(attr)
        await db.flush()

    return await db.commit()


async def get_pagination(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = (
        select(AttrInDb)
        .offset(skip)
        .limit(limit)
    )

    data = (await db.execute(query)).scalars().all()
    return data