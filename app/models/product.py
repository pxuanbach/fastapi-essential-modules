from enum import Enum
from typing import List, Optional
import uuid as uuid_pkg
from datetime import datetime
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import DateTime, func
from sqlalchemy.orm import relationship

from app.models.resource import ResourceInDb


class ProductBase(SQLModel):
    name: str
    slug: str
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


class Product(ProductBase):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        index=True, 
        primary_key=True,
        nullable=False
    )

    model_config = ConfigDict(from_attributes=True)


class ProductInDb(Product, table=True):
    __tablename__ = "products"

    resources: List[ResourceInDb] = Relationship(
        sa_relationship=relationship(
            "ResourceInDb",
            primaryjoin="and_(foreign(ResourceInDb.object_id)==ProductInDb.id, ResourceInDb.object_type=='product')",
            viewonly=True,
        )
    )

    @classmethod
    def create(
        cls,
        name: str,
        slug: str,
    ) -> "ProductInDb":
        return cls(
            name=name,
            slug=slug,
        )
