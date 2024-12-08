from enum import Enum
from typing import Optional
import uuid as uuid_pkg
from datetime import datetime
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel
from sqlalchemy import DateTime, func

from app.enums.resource import ResourceObjectType


class ResourceBase(SQLModel):
    filename: str
    filepath: str
    object_type: ResourceObjectType
    object_id: uuid_pkg.UUID
    created_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": func.now(), "server_default": func.now()},
    )


class Resource(ResourceBase):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        index=True, 
        primary_key=True,
        nullable=False
    )

    model_config = ConfigDict(from_attributes=True)


class ResourceInDb(Resource, table=True):
    __tablename__ = "resources"

    @classmethod
    def create(
        cls,
        filename: str,
        filepath: str,
        object_type: ResourceObjectType,
        object_id: uuid_pkg.UUID,
    ) -> "ResourceInDb":
        return cls(
            filename=filename,
            filepath=filepath,
            object_type=object_type,
            object_id=object_id,
        )


# class UserResource(ResourceInDb):
#     __mapper_args__ = {
#         "polymorphic_identity": "user",
#     }


# class ProductResource(ResourceInDb):
#     __mapper_args__ = {
#         "polymorphic_identity": "user",
#     }
