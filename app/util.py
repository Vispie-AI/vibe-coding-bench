import hashlib
import itertools

_counter = itertools.count(1)


def new_id(prefix: str) -> str:
    return f"{prefix}_{next(_counter)}"


def vec_from_text(text: str, quality: float) -> list[float]:
    """Derive an 8-dim style vector from generated text.

    `quality` (0..1) scales fidelity — a lower-quality generation yields a
    weaker, noisier style signal.
    """
    h = hashlib.sha1(text.encode("utf-8")).digest()
    base = [b / 255.0 for b in h[:8]]
    return [round(x * quality, 4) for x in base]


def blend(prior: list[float], fresh: list[float], w: float) -> list[float]:
    """Blend prior style with fresh output; w = weight kept on prior."""
    return [round(w * a + (1 - w) * b, 4) for a, b in zip(prior, fresh)]


def drift(a: list[float], b: list[float]) -> float:
    """L2 distance between two style vectors (not used in the hot path)."""
    return round(sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5, 4)
