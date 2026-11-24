import os
from dataclasses import dataclass

INDONESIA_BBOX = "95,-11,141,6"  # west,south,east,north

CITIES = {
    "Jakarta": (-6.2088, 106.8456),
    "Palembang": (-2.9761, 104.7754),
    "Pontianak": (-0.0263, 109.3425),
    "Banjarmasin": (-3.3186, 114.5944),
    "Balikpapan": (-1.2379, 116.8529),
    "Makassar": (-5.1477, 119.4327),
    "Manado": (1.4748, 124.8421),
    "Jayapura": (-2.5916, 140.6690),
}


@dataclass(frozen=True)
class Settings:
    firms_map_key: str | None
    firms_source: str
    firms_bbox: str
    azure_storage_account: str | None
    azure_storage_container: str
    output_dir: str

    @classmethod
    def load(cls) -> "Settings":
        return cls(
            firms_map_key=os.getenv("FIRMS_MAP_KEY"),
            firms_source=os.getenv("FIRMS_SOURCE", "VIIRS_SNPP_NRT"),
            firms_bbox=os.getenv("FIRMS_BBOX", INDONESIA_BBOX),
            azure_storage_account=os.getenv("AZURE_STORAGE_ACCOUNT"),
            azure_storage_container=os.getenv("AZURE_STORAGE_CONTAINER", "scraping-results"),
            output_dir=os.getenv("OUTPUT_DIR", "data"),
        )