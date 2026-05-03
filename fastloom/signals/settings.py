from pydantic import AmqpDsn, BaseModel

from fastloom.types import Str
from fastloom.vault.settings import VaultBackend


class RabbitmqSettings(BaseModel):
    RABBIT_URI: VaultBackend[Str[AmqpDsn]]
