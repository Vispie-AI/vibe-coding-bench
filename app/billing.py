"""Usage billing (cents)."""

RATE = 0.07  # cents per output character


def charge(length: int) -> int:
    """Cost in whole cents for a generation of the given output length."""
    return int(length * RATE)
