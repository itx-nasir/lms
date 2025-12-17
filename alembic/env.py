import os
from logging.config import fileConfig
from dotenv import load_dotenv

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Load .env from project root so env vars (DATABASE_URL or DB_*) are available
repo_root = os.path.dirname(os.path.dirname(__file__))
env_path = os.path.join(repo_root, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# add your model's MetaData object here for 'autogenerate' support
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models import Base

target_metadata = Base.metadata

# get DB URL from env
database_url = os.getenv('DATABASE_URL')
if not database_url:
    # fallback built into app's .env may specify DB components
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME')
    if db_user and db_password and db_name:
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    else:
        database_url = os.getenv('SQLALCHEMY_DATABASE_URL', 'sqlite:///./lms.db')

config.set_main_option('sqlalchemy.url', database_url)


def run_migrations_offline():
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
