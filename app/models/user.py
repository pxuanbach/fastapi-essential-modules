from typing import List, Optional
import uuid as uuid_pkg
from sqlmodel import Field, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    full_name: str | None = None


class User(UserBase):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        index=True, 
        primary_key=True,
        nullable=False
    )
    is_superuser: bool = False

    class Config:
       read_with_orm_mode = True 


class UserInDb(User, table=True):
    __tablename__ = "users"

    hashed_password: str

    @classmethod
    def create(
        cls,
        email: str,
        hashed_password: str,
        is_active: bool = False,
        is_superuser: bool = False,
        full_name: Optional[str] = None
    ) -> "UserInDb":
        return cls(
            hashed_password=hashed_password,
            email=email,
            full_name=full_name,
            is_active=is_active,
            is_superuser=is_superuser
        )


class UserView(User):
    class AttrView(SQLModel):
        title: Optional[str]
        # id: Optional[uuid_pkg.UUID]
        # link_id: Optional[uuid_pkg.UUID]
    
    attrs: List[AttrView]

    