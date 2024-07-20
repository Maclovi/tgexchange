from dataclasses import dataclass
from os import environ


@dataclass(frozen=True)
class RedisConf:
    host: str
    port: str
    db: str
    password: str

    def get_uri(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


@dataclass(frozen=True)
class TgBot:
    token: str
    debug: bool


@dataclass(frozen=True)
class Config:
    tg_bot: TgBot
    redis: RedisConf


def load_config() -> Config:
    return Config(
        tg_bot=TgBot(
            token=environ["TOKEN"],
            debug=bool(environ["DEBUG_BOT"]),
        ),
        redis=RedisConf(
            host=environ.get("REDIS_HOST", "localhost"),
            port=environ["REDIS_PORT"],
            db=environ["REDIS_DB"],
            password=environ["REDIS_PASSWORD"],
        ),
    )
