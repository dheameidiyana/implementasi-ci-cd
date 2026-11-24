import csv
import io
import logging
from datetime import date, timedelta

import requests

from src.config import Settings

log = logging.getLogger(__name__)

FIRMS_AREA_URL = (
    "https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
    "{key}/{source}/{bbox}/{days}/{start_date}"
)


def fetch_firms(settings: Settings, session: requests.Session | None = None) -> list[dict]:
    if not settings.firms_map_key:
        log.warning("FIRMS_MAP_KEY belum di-set, NASA FIRMS dilewati")
        return []

    start = (date.today() - timedelta(days=1)).isoformat()
    url = FIRMS_AREA_URL.format(
        key=settings.firms_map_key,
        source=settings.firms_source,
        bbox=settings.firms_bbox,
        days=1,
        start_date=start,
    )
    client = session or requests.Session()
    resp = client.get(url, timeout=60)
    resp.raise_for_status()

    if "Invalid" in resp.text[:200] or not resp.text.strip():
        raise RuntimeError(f"Respons FIRMS tidak valid: {resp.text[:200]}")

    rows = []
    for row in csv.DictReader(io.StringIO(resp.text)):
        row["source"] = "NASA_FIRMS"
        rows.append(row)

    log.info("FIRMS: %d hotspot diterima", len(rows))
    return rows