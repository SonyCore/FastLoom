from typing import Annotated

from pydantic import BeforeValidator, Field

from fastloom.settings.utils import pydantic_vault_or_default

type VaultBackend[T] = Annotated[
    T, BeforeValidator(pydantic_vault_or_default("VAULT_FILE"))
]


def VaultDefault[T](default: T):
    return Field(default=default, validate_default=True)
