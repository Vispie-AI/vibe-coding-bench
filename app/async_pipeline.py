"""Async post-generation pipeline — runs after each generate (warm trending, notify)."""
import asyncio
import time

_trending: list = []


async def _warm_trending(item_id: str) -> None:
    await asyncio.sleep(0)
    _trending.append(item_id)


def _notify(item_id: str) -> None:
    # post to the notifications service (sync client) — ~50ms round trip
    time.sleep(0.05)


async def post_generate(item_id: str) -> None:
    await _warm_trending(item_id)
    _notify(item_id)
