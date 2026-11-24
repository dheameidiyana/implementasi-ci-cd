import logging

import requests

from src.config import CITIES, Settings

log = logging.getLogger(__name__)

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
    "wind_direction_10m",
]


def fetch_weather(
    settings: Settings, session: requests.Session | None = None
) -> list[dict]:
    client = session or requests.Session()
    results = []

    for city, (lat, lon) in CITIES.items():
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ",".join(WEATHER_VARS),
            "timezone": "Asia/Jakarta",
            "forecast_days": 1,
        }
        resp = client.get(WEATHER_URL, params=params, timeout=60)
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
        log.info("Weather: %s OK", city)

    return results