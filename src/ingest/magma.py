import logging

import requests

from src.config import Settings

log = logging.getLogger(__name__)

MAGMA_URL = "https://magma.esdm.go.id/v1/gunung-api/aktivitas"


def fetch_magma(
    settings: Settings, session: requests.Session | None = None
) -> list[dict]:
    client = session or requests.Session()
    try:
        resp = client.get(
            MAGMA_URL,
            timeout=60,
            headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"},
        )
        resp.raise_for_status()
        payload = resp.json()
        rows = payload if isinstance(payload, list) else payload.get("data", [])
        log.info("MAGMA: %d aktivitas diterima", len(rows))
        return rows
    except Exception as exc:
        log.warning("MAGMA tidak tersedia (%s), dilewati", exc)
        return []