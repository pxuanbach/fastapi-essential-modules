from typing import Optional
import uuid as uuid_pkg
from sqlmodel import Field, SQLModel


class UserDetailBase(SQLModel):
    user_id: uuid_pkg.UUID | None = Field(default=None, foreign_key="users.id") 
    address: str | None


class UserDetail(UserDetailBase):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        index=True, 
        primary_key=True,
        nullable=False
    )

    class Config:
       read_with_orm_mode = True 


class UserDetailInDb(UserDetail, table=True):
    __tablename__ = "user_details"

    @classmethod
    def create(
        cls,
        user_id: Optional[uuid_pkg.UUID] = None,
        address: Optional[str] = None,
    ) -> "UserDetailInDb":
        return cls(
            user_id=user_id,
            address=address
        )


