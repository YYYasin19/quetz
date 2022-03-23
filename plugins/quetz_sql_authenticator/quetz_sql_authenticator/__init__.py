import secrets

from sqlmodel import Session, create_engine, select

from quetz.authentication.base import SimpleAuthenticator
from quetz.config import Config, ConfigEntry, ConfigSection

from .utils import Credentials, calculate_hash


class UsernameNotFound(RuntimeError):
    """Error that is thrown when the username is not found."""


def _get_password_hashed(username_hashed: str, session: Session) -> str:
    result = session.exec(
        select(Credentials).where(Credentials.username == username_hashed)
    ).first()
    if result:
        return result.password
    raise UsernameNotFound(username_hashed)


_CONFIG_NAME = "sql_authenticator"

_CONFIG = [
    ConfigSection(
        _CONFIG_NAME,
        [
            ConfigEntry(
                name="database_url",
                cast=str,
                required=True,
            )
        ],
    )
]


class SQLAuthenticator(SimpleAuthenticator):
    """An authenticator that uses a SQLAlchemy backend."""

    provider = "sql"

    def configure(self, config: Config):
        """Configure."""
        config.register(_CONFIG)

        if config.configured_section(_CONFIG_NAME):
            self._engine = create_engine(
                getattr(config, f"{_CONFIG_NAME}_database_url")
            )
            self.is_enabled = True

        super().configure(config)

    async def authenticate(self, request, data, **kwargs):
        """Authenticate."""
        with Session(self._engine) as session:
            try:
                password_hashed = _get_password_hashed(
                    calculate_hash(data["username"]), session
                )
            except UsernameNotFound:
                password_hashed = ""
        if secrets.compare_digest(calculate_hash(data["password"]), password_hashed):
            return data["username"]
