import json
import random
from sqlmodel import SQLModel, select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import UserInDb
from app.models.user_attr import UserAttrInDb
from app.models.attr import AttrInDb
from app.utils import generate_random_string


def create_view():
    view = (
        select(
            UserInDb.id,
            UserInDb.full_name,
            UserInDb.email,
            UserInDb.is_superuser,
            func.jsonb_agg(
                func.jsonb_build_object(
                    "title", AttrInDb.title,
                    # "id", AttrInDb.id,
                    # "link_id", UserAttrInDb.id,
                )
            ).label("attrs")
        )
        .outerjoin(UserAttrInDb, UserAttrInDb.user_id == UserInDb.id)
        .join(AttrInDb, AttrInDb.id == UserAttrInDb.attr_id)
        .group_by(UserInDb.id)
    )
    return view


async def bulk_insert(db: AsyncSession, n=1000):
    email_tail = [
        "gmail.com", "outlook.com", "google.com", "tisoha.com", "yahoo.com", "microsoft.com", 
        "zoho.com", "icloud.com", "gm.uit.edu.vn", "tdtu.edu.vn", "tsh.com"
    ]
    full_names = [
        "Phạm Xuân Bách", "Trương Gia Thạch", "Bách Phạm", "Trương Gia Huy", "Cao Quảng An Hưng", 
        "Võ Quốc Minh", "Thạch Trương", "Nguyễn Khánh Toàn", "Olivor Hung", "James Nguyen", "Đặng Hải Thịnh",
        "Thịnh Đặng", "Darious Đặng", "Lê Hoàng Phú", "Phú Lê", "Đỗ Công Bá", "Nemo Do", "Dương Hoài Nam", 
        "Nam Dương", "Võ Hoàng Đức Khoa", "Khoa Võ", "Otis Võ", "Trần Nhật An", "Nguyễn Văn Biên",
        "Kafka", "Lucian Nguyen", "Phan Đức Thanh Duy", "Nguyễn Trần Quốc Duy", "Hoàng Nguyễn Phúc Nguyên Chương",
        "Võ Tiến Khoa", "Bùi Minh Nhật", "Tăng Du Linh", "Võ Thị Bích Loan", "Phạm Ngọc Thanh Thảo",
        "Lý Hùng Trọng", "Nguyễn Hoàng Minh", "Bùi Dương Tuấn", "Đinh Vương Bảo", " Nguyễn Thị Quỳnh Hoa"
    ]

    for i in range(n):
        user = UserInDb.create(
            email=generate_random_string() + "_" + generate_random_string(5) + "@" + email_tail[random.randrange(0, len(email_tail)-1)],
            hashed_password=generate_random_string(),
            full_name=full_names[random.randrange(0, len(full_names)-1)]
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


async def get_pagination_view(db: AsyncSession, skip: int = 0, limit: int = 10):
    view  = create_view()
    query = (
        view
        .offset(skip)
        .limit(limit)
    )

    data = (await db.execute(query)).all()
    return data
