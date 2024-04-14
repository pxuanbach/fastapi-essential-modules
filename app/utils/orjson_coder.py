from typing import Any
from fastapi.encoders import jsonable_encoder
import orjson


class ORJsonCoder:
    def encode(cls, value: Any) -> bytes:
        return orjson.dumps(
            value,
            default=jsonable_encoder,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        )

    def decode(cls, value: bytes) -> Any:
        return orjson.loads(value)