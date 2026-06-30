"""A small object cache. Values are serialized so they can move to Redis later."""
import pickle
from typing import Any, Dict

_BLOBS: Dict[str, bytes] = {}


def put(key: str, value: Any) -> None:
    _BLOBS[key] = pickle.dumps(value)


def get(key: str) -> Any:
    blob = _BLOBS.get(key)
    return pickle.loads(blob) if blob is not None else None
