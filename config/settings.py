import os
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field


class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_base_url: str
    frontend_base_url: str

    api_timeout_ms: int = Field(
        gt=0,
        le=120_000,
    )
    ui_timeout_ms: int = Field(
        gt=0,
        le=120_000,
    )


def load_settings() -> Settings:
    environment = os.getenv("TEST_ENV", "local")

    config_dir = Path(__file__).parent / "environments"
    config_path = config_dir / f"{environment}.yaml"

    if not config_path.exists():
        available_environments = sorted(
            path.stem
            for path in config_dir.glob("*.yaml")
        )

        raise ValueError(
            f"Unknown test environment: {environment}. "
            f"Available environments: "
            f"{', '.join(available_environments)}"
        )

    with config_path.open(encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if config is None:
        raise ValueError(
            f"Configuration file is empty: {config_path}"
        )

    if not isinstance(config, dict):
        raise ValueError(
            f"Configuration root must be a mapping: {config_path}"
        )

    return Settings.model_validate(config)


settings = load_settings()