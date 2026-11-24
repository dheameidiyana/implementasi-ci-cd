import logging

import requests

from src.config import CITIES, Settings

log = logging.getLogger(__name__)

AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
AIR_QUALITY_VARS = [
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
    "us_aqi",
]


def fetch_air_quality(
    settings: Settings, session: requests.Session | None = None
) -> list[dict]:
    client = session or requests.Session()
    results = []

    for city, (lat, lon) in CITIES.items():
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ",".join(AIR_QUALITY_VARS),
            "timezone": "Asia/Jakarta",
            "forecast_days": 1,
        }
        resp = client.get(AIR_QUALITY_URL, params=params, timeout=60)
        resp.raise_for_status()
        payload = resp.json()
        results.append(
            {
                "city": city,
                "latitude": lat,
                "longitude": lon,
                "hourly": payload.get("hourly", {}),
            }
        )
        log.info("AirQuality: %s OK", city)

    return results