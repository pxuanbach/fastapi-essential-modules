from typing import Optional
import uuid as uuid_pkg
from sqlmodel import Field, SQLModel


class AttrBase(SQLModel):
    title: str | None = None 


class Attr(AttrBase):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        index=True, 
        primary_key=True,
        nullable=False
    )

    class Config:
       read_with_orm_mode = True 


class AttrInDb(Attr, table=True):
    __tablename__ = "attrs"

    @classmethod
    def create(
        cls,
        title: Optional[str] = None,
    ) -> "AttrInDb":
        return cls(
            title=title
        )
