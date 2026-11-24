from src.config import Settings
from src.ingest import magma


def make_settings() -> Settings:
    return Settings(
        None, "VIIRS_SNPP_NRT", "95,-11,141,6", None, "scraping-results", "data"
    )


class OkResponse:
    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return {"data": [{"gunung": "Merapi", "level": "Waspada"}]}


class OkSession:
    def get(self, *args, **kwargs) -> OkResponse:
        return OkResponse()


class FailSession:
    def get(self, *args, **kwargs):
        raise RuntimeError("down")


def test_fetch_magma_ok() -> None:
    rows = magma.fetch_magma(make_settings(), session=OkSession())
    assert rows[0]["gunung"] == "Merapi"


def test_fetch_magma_graceful_on_error() -> None:
    assert magma.fetch_magma(make_settings(), session=FailSession()) == []