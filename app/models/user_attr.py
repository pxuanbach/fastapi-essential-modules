from typing import Optional
import uuid as uuid_pkg
from sqlmodel import Field, SQLModel


class UserAttrBase(SQLModel):
    user_id: uuid_pkg.UUID | None = Field(default=None, foreign_key="users.id") 
    attr_id: uuid_pkg.UUID | None = Field(default=None, foreign_key="attrs.id") 


class UserAttr(UserAttrBase):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        index=True, 
        primary_key=True,
        nullable=False
    )

    class Config:
       read_with_orm_mode = True 


class UserAttrInDb(UserAttr, table=True):
    __tablename__ = "user_attrs"

    @classmethod
    def create(
        cls,
        user_id: Optional[uuid_pkg.UUID] = None,
        attr_id: Optional[uuid_pkg.UUID] = None,
    ) -> "UserAttrInDb":
        return cls(
            user_id=user_id,
            attr_id=attr_id
        )


