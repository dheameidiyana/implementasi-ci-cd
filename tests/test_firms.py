from src.config import Settings
from src.ingest import firms


def make_settings(key: str | None = "dummy") -> Settings:
    return Settings(
        firms_map_key=key,
        firms_source="VIIRS_SNPP_NRT",
        firms_bbox="95,-11,141,6",
        azure_storage_account=None,
        azure_storage_container="scraping-results",
        output_dir="data",
    )


class FakeResponse:
    def __init__(self, text: str) -> None:
        self.text = text

    def raise_for_status(self) -> None:
        return None


class FakeSession:
    def __init__(self, text: str) -> None:
        self.text = text

    def get(self, *args, **kwargs) -> FakeResponse:
        return FakeResponse(self.text)


def test_fetch_firms_parses_csv() -> None:
    csv_text = (
        "latitude,longitude,bright_ti4,acq_date\n"
        "-1.2,110.3,330.1,2026-11-24\n"
    )
    rows = firms.fetch_firms(make_settings(), session=FakeSession(csv_text))
    assert len(rows) == 1
    assert rows[0]["source"] == "NASA_FIRMS"


def test_fetch_firms_without_key_returns_empty() -> None:
    assert firms.fetch_firms(make_settings(key=None)) == []