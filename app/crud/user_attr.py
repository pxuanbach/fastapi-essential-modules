import random
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user_attr import UserAttrInDb
from app.models.attr import AttrInDb
from .attr import get_pagination as get_attr_pagi
from .user import get_pagination as get_user_pagi


async def bulk_insert(db: AsyncSession, n=1000):
    users = await get_user_pagi(db, 0, n)
    attrs = await get_attr_pagi(db, 0, 200)

    for i in range(len(users)):
        attr: AttrInDb = attrs[random.randrange(0, len(attrs)-1)]
        user_attr = UserAttrInDb.create(
            user_id=users[i].id,
            attr_id=attr.id
        )
        db.add(user_attr)
        if i%2 == 1:
            user_attr = UserAttrInDb.create(
                user_id=users[i].id,
                attr_id=attrs[random.randrange(0, len(attrs)-1)].id
            )
            db.add(user_attr)
        await db.flush()

    return await db.commit()
