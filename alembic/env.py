from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool


import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))
# ---------------------------------------------------------------


from core.config import settings       
from db.base import Base               


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadatos de tus modelos (necesarios para autogenerate)
target_metadata = Base.metadata


def run_migrations_offline():
    """Ejecuta migraciones en modo 'offline'."""
    url = settings.SQLALCHEMY_DATABASE_URI
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Ejecuta migraciones en modo 'online' (conectado a la DB)."""
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = settings.SQLALCHEMY_DATABASE_URI

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# --- Ejecutar según el modo de Alembic ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
