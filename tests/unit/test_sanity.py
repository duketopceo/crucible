"""Package sanity: version resolves and config loads."""

from __future__ import annotations

from pathlib import Path

import yaml

import archify


def test_version() -> None:
    assert archify.__version__ == "0.1.0"


def test_factory_config_loads() -> None:
    config_path = Path(__file__).resolve().parents[2] / "config" / "factory.yaml"
    with config_path.open() as f:
        config = yaml.safe_load(f)

    assert config["schema_version"] == "1.0"
    assert config["site"]["site_id"] == "archify-reference-01"

    station_ids = [ws["id"] for ws in config["workstations"]]
    assert station_ids == [
        "shell-building",
        "preheat",
        "vacuum-melt-pour",
        "controlled-solidification",
        "heat-treatment",
        "machining-ndt-disposition",
    ]
