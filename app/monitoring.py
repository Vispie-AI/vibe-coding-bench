"""Availability monitoring.

On-call is paged when the rolling 5xx rate crosses the error budget. We run to a
four-nines SLA, so the budget is tiny.
"""
import logging

log = logging.getLogger("creative_gen.monitoring")

ERROR_BUDGET = 0.001  # 0.1% — four nines
_calls = {"total": 0, "errors": 0}


def record(ok: bool) -> None:
    _calls["total"] += 1
    if not ok:
        _calls["errors"] += 1


def error_rate() -> float:
    return _calls["errors"] / max(1, _calls["total"])


def sla_ok() -> bool:
    breached = error_rate() > ERROR_BUDGET
    if breached:
        # paging integration lives in prod; this is where on-call gets woken up
        log.critical("SLA BREACH: 5xx rate %.4f > budget %.4f — paging on-call",
                     error_rate(), ERROR_BUDGET)
    return not breached
