from src.config import Settings
from src.ingest import weather


def make_settings() -> Settings:
    return Settings(
        None, "VIIRS_SNPP_NRT", "95,-11,141,6", None, "scraping-results", "data"
    )


class FakeResponse:
    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return {"hourly": {"temperature_2m": [28.5]}}


class FakeSession:
    def get(self, *args, **kwargs) -> FakeResponse:
        return FakeResponse()


def test_fetch_weather_returns_all_cities() -> None:
    rows = weather.fetch_weather(make_settings(), session=FakeSession())
    assert len(rows) == 8
    assert rows[0]["hourly"]["temperature_2m"] == [28.5]