"""Postgres durable store.

The in-memory structures in store.py are the hot working set (and where the
application logic lives). This module mirrors durable writes to Postgres so the
service has a real, queryable database. If DATABASE_URL is unset or unreachable,
every call degrades to a no-op — the service runs fine without a DB (used by
the offline test harness).
"""
import logging
import os

log = logging.getLogger("creative_gen.db")

_DATABASE_URL = os.getenv("DATABASE_URL", "")
_pool = None
_enabled = None


def _conn():
    global _pool, _enabled
    if _enabled is False:
        return None
    if not _DATABASE_URL:
        _enabled = False
        return None
    if _pool is None:
        try:
            import psycopg_pool  # type: ignore
            _pool = psycopg_pool.ConnectionPool(_DATABASE_URL, min_size=1, max_size=8, open=True)
            _enabled = True
            log.info("postgres pool ready")
        except Exception as e:  # noqa: BLE001
            log.warning("postgres unavailable, running without DB: %s", e)
            _enabled = False
            return None
    return _pool


def init_db() -> None:
    conn = _conn()
    if conn is None:
        return
    with conn.connection() as c:
        with open(os.path.join(os.path.dirname(__file__), "..", "db", "init.sql")) as f:
            c.execute(f.read())


def insert_item(item_id: str, creator_id: str, caption: str, hook: str,
                performance: float, served_by) -> None:
    conn = _conn()
    if conn is None:
        return
    try:
        with conn.connection() as c, c.cursor() as cur:
            cur.execute(
                """INSERT INTO items (item_id, creator_id, caption, hook, performance, served_by)
                   VALUES (%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (item_id) DO UPDATE SET
                     caption=EXCLUDED.caption, hook=EXCLUDED.hook,
                     performance=EXCLUDED.performance, served_by=EXCLUDED.served_by""",
                (item_id, creator_id, caption, hook, performance, served_by),
            )
    except Exception as e:  # noqa: BLE001
        log.debug("insert_item failed: %s", e)


def count_items() -> int:
    conn = _conn()
    if conn is None:
        return -1
    try:
        with conn.connection() as c, c.cursor() as cur:
            cur.execute("SELECT count(*) FROM items")
            return cur.fetchone()[0]
    except Exception:  # noqa: BLE001
        return -1
