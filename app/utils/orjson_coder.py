from datetime import datetime
import decimal
from json import JSONEncoder
from typing import Any, Union
from uuid import UUID
from fastapi.encoders import jsonable_encoder
import orjson


class ORJsonCoder:
    def encode(cls, value: Any) -> bytes:
        return orjson.dumps(
            value,
            default=jsonable_encoder,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        )

    def decode(cls, value: Union[bytes | str]) -> Any:
        return orjson.loads(value)


def init_json_encode():
    old_default = JSONEncoder.default

    def new_default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, datetime):
            return str(obj)
        return old_default(self, obj)
    
    JSONEncoder.default = new_default
    