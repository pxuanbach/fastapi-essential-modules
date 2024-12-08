from enum import Enum


class ResourceObjectType(str, Enum):
    BASE = "base"
    PRODUCT = "product"
    USER = "user"
