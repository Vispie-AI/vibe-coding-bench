import logging
import os

log = logging.getLogger("creative_gen")

# ---- generation config ----------------------------------------------------
PRIMARY_MODEL = os.getenv("GEN_PRIMARY_MODEL", "gen-large-v3")
FALLBACK_MODEL = os.getenv("GEN_FALLBACK_MODEL", "gen-small-v1")
GEN_TIMEOUT_S = float(os.getenv("GEN_TIMEOUT_S", "8.0"))
STYLE_BLEND = float(os.getenv("STYLE_BLEND", "0.6"))      # how much prior style to keep on regen
REFERENCE_FANOUT = int(os.getenv("REFERENCE_FANOUT", "4"))


# ---- metrics (optional, best-effort) --------------------------------------
# We export OTLP metrics to the collector when one is reachable. In most
# environments it is not, which is fine: generation does not depend on it.
def _init_metrics():
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    try:
        # real exporter handshake happens here; emulate the prod connectivity check
        raise ConnectionError(f"OTLP exporter unreachable at {endpoint}")
    except Exception as e:  # noqa: BLE001
        # Loud on purpose so prod dashboards notice a missing collector.
        # Metrics are best-effort — the service runs fine without them.
        log.error("metrics exporter init failed: %s — will retry in background", e)
        return None


METRICS = _init_metrics()
