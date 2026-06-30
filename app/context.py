"""Per-request context — the current actor (creator) for the in-flight request."""

_state = {}  # process-wide; set at request entry, read by downstream helpers


def set_actor(creator_id: str) -> None:
    _state["actor"] = creator_id


def current_actor() -> str:
    return _state.get("actor", "")
