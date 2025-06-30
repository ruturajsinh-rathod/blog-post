import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.engine import Connection

from apps import Base
from config import settings
from core.db import engine

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table="auth_alembic_version",
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
        await connection.commit()
    await engine.dispose()


if context.is_offline_mode():
    raise NotImplementedError("Offline migrations are not supported")
else:
    asyncio.run(run_async_migrations())
