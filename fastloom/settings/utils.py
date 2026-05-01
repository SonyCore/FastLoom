from collections.abc import Callable
from os import getenv
from pathlib import Path
from typing import Any

from pydantic import ValidationInfo


def get_env_or_err(field_name: str) -> Callable[[], str]:
    def _inner() -> str:
        value = getenv(field_name)
        if value is None:
            raise ValueError(
                f"{field_name} must be set in environment or config"
            )
        return value

    return _inner


def pydantic_env_or_default(v: Any, info: ValidationInfo) -> Any:
    if info.field_name is None:
        return v
    return getenv(info.field_name, v)


def read_vault_field(path: Path, field_name: str) -> str | None:
    if not path.exists():
        return None
    for line in path.read_text().splitlines():
        key, _, value = line.partition("=")
        if key.strip() == field_name:
            return value.strip()
    return None


def pydantic_vault_or_default(
    env_name: str,
) -> Callable[[Any, ValidationInfo], Any]:
    def _inner(v: Any, info: ValidationInfo) -> Any:
        if info.field_name is None:
            return v
        vault_file = getenv(env_name)
        if vault_file:
            value = read_vault_field(Path(vault_file), info.field_name)
            if value is not None:
                return value
        return getenv(info.field_name, v)

    return _inner
