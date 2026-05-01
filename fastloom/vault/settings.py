from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    PostgresDsn,
)

from fastloom.settings.utils import pydantic_vault_or_default
from fastloom.types import Str

type VaultBackend[T] = Annotated[
    T, BeforeValidator(pydantic_vault_or_default("VAULT_FILE"))
]


def VaultDefault[T](default: T):
    return Field(default=default, validate_default=True)


class PostgresConfig(BaseModel):
    POSTGRES_DSN: VaultBackend[Str[PostgresDsn]] | None = VaultDefault(None)
    POOL_SIZE: int = 50
    MAX_OVERFLOW: int = 20


class FastStreamConfig(BaseModel): ...


class BeanieConfig(BaseModel): ...


class VaultSettings(PostgresConfig):
    pass
