from typing import List, Optional
import uuid as uuid_pkg
from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.orm import relationship

from app.models.resource import ResourceInDb


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

    model_config = ConfigDict(from_attributes=True)


class UserInDb(User, table=True):
    __tablename__ = "users"

    hashed_password: str

    resources: List[ResourceInDb] = Relationship(
        sa_relationship=relationship(
            "ResourceInDb",
            primaryjoin="and_(foreign(ResourceInDb.object_id)==UserInDb.id, ResourceInDb.object_type=='user')",
            viewonly=True,
        )
    )

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
