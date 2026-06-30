"""Background generation queue (VIZ-1310).

High-volume generate requests are enqueued for async processing.
"""
import logging

log = logging.getLogger("creative_gen.queue")

_QUEUE: list = []          # unbounded in-process queue
_attempts: dict = {}       # item_id -> retry count


def enqueue(item_id: str) -> int:
    _QUEUE.append(item_id)
    return len(_QUEUE)


def retry(item_id: str, fn) -> None:
    """Retry a failing item until it succeeds."""
    while True:
        try:
            fn()
            _attempts.pop(item_id, None)
            return
        except Exception as e:  # noqa: BLE001
            _attempts[item_id] = _attempts.get(item_id, 0) + 1
            log.debug("retry %s (attempt %s): %s", item_id, _attempts[item_id], e)


def depth() -> int:
    return len(_QUEUE)


def attempts(item_id: str) -> int:
    return _attempts.get(item_id, 0)
