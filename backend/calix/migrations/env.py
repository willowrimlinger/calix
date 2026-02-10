import logging
from logging.config import fileConfig
from shutil import which
import subprocess

from flask import current_app

from alembic import context
from sqlalchemy import text

import calix.migrations.enum_migration

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    try:
        return get_engine().url.render_as_string(hide_password=False).replace(
            '%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata

def include_name(name, type_, parent_names):
    """
    Protects the alembic_version_history table from being overwritten, as it does not exist in code.
    This table contains more info about the state of your database and which migrations have run.
    It's intended to aid in those situations where you forgot to downgrade and you can't
    remember which git branch the migration is on.

    Credit to: https://stackoverflow.com/questions/73248731/alembic-store-extra-information-in-alembic-version-table
    """
    if type_ == "table":
        if name == "alembic_version_history":
            return False
    return True

def get_git_info() -> tuple[str | None, str | None]:
    # check if git is installed
    if not which("git"):
        return None, None

    # get info
    git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True)
    git_branch_name = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True)
    return git_commit, git_branch_name

def update_history(ctx, step, heads, run_args):
    """Creates and updates the alembic_version_history table"""
    ctx.connection.execute(text("""
    CREATE TABLE IF NOT EXISTS alembic_version_history (
        version_num VARCHAR(32) NOT NULL,
        inserted_at TIMESTAMP NOT NULL,
        migration_message TEXT NOT NULL,
        git_commit VARCHAR(40) NULL,
        git_branch_name TEXT NULL
    )
    """))
    revision_id = step.up_revision_id
    if step.is_upgrade:
        message = step.up_revision.doc
        git_commit, git_branch_name = get_git_info()
        ctx.connection.execute(text(
            f"INSERT INTO alembic_version_history (version_num, inserted_at, migration_message, git_commit, git_branch_name) VALUES ('{revision_id}' ,NOW(), '{message}', '{git_commit}', '{git_branch_name}')"
        ))
    else:
        ctx.connection.execute(text(f"DELETE FROM alembic_version_history where version_num = '{revision_id}'"))


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=get_metadata(),
        literal_binds=True,
        include_name=include_name,
        on_version_apply=update_history,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            include_name=include_name,
            on_version_apply=update_history,
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
