import argparse
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from src.config import Settings
from src.ingest import air_quality, firms, magma, weather
from src.storage.azure_blob import upload_file

log = logging.getLogger("pipeline")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pipeline ingestion data")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="jalankan tanpa upload ke Azure Blob Storage",
    )
    return parser.parse_args()


def write_json(payload: dict, out_dir: Path, source: str, stamp: datetime) -> Path:
    folder = out_dir / "raw" / source / f"dt={stamp:%Y-%m-%d}" / f"hour={stamp:%H}"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{source}_{stamp:%Y%m%dT%H%M%SZ}.json"
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return path


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    args = parse_args()
    settings = Settings.load()
    stamp = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    out_dir = Path(settings.output_dir)

    collectors = {
        "firms": lambda: firms.fetch_firms(settings),
        "magma": lambda: magma.fetch_magma(settings),
        "air_quality": lambda: air_quality.fetch_air_quality(settings),
        "weather": lambda: weather.fetch_weather(settings),
    }

    manifest = {"run_utc": datetime.now(timezone.utc).isoformat(), "sources": {}}

    for name, collect in collectors.items():
        try:
            data = collect()
        except Exception as exc:
            log.error("%s gagal: %s", name, exc)
            data = []

        payload = {"source": name, "run_utc": manifest["run_utc"], "records": data}
        path = write_json(payload, out_dir, name, stamp)
        entry = {"records": len(data), "file": str(path)}

        if not args.dry_run and settings.azure_storage_account:
            blob_name = (
                f"raw/{name}/dt={stamp:%Y-%m-%d}/hour={stamp:%H}/{path.name}"
            )
            entry["blob"] = upload_file(path, blob_name)

        manifest["sources"][name] = entry

    manifest_path = write_json(manifest, out_dir, "manifest", stamp)
    print(json.dumps(manifest, indent=2))
    log.info("Manifest: %s", manifest_path)


if __name__ == "__main__":
    main()