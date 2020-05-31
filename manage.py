from alembic.config import Config as alembic_config_class
from alembic import command as alembic_command
# alembic setup
alembic_config = alembic_config_class('db/alembic.ini')
import os
import click
from time import sleep

# pep8 setup
cwd = os.path.dirname(os.path.realpath(__file__))
_pep8_excluded_patterns = []


@click.group()
def cli():
    pass


# @click.command()
# @click.argument('port', default=5000)
# def run(port):
#     """ Run the development server.
#     """
#     app = main.create_app()
#     app.run(host="0.0.0.0", port=port, debug=True)

# @click.command()
# def daemon():
#     """
#     Lets listen.
#     """
#     NotificationDaemon().consume()

# @click.command()
# def cron():
#     """
#     Lets listen.
#     """
#     while True:        
#         run_cron()
#         sleep(60)

# namespace for db commands
@click.group()  # noqa
def db():
    """ Schema related commands.
    """
    pass

@db.command()
@click.option(
    '--revision',
    default='head',
    help="the revision to upgrade to. defaults to head."
)
@click.option('--sql', is_flag=True)
def upgrade(revision, sql):
    """ Upgrade database to a revision
    """
    alembic_command.upgrade(alembic_config, revision, sql=sql)


@db.command()
@click.option(
    '--revision',
    required=True,
    help="the revision to downgrade to."
)
@click.option('--sql', is_flag=True)
def downgrade(revision, sql):
    """ Downgrade database to a revision
    """
    alembic_command.downgrade(alembic_config, revision, sql=sql)


@db.command()
@click.option(
    '--message',
    '-m',
    required=True,
    help="description of this schema change."
)
def revision(message):
    """ Generate a schema change from model changes
    """
    alembic_command.revision(
        alembic_config,
        message=message,
        autogenerate=True
    )


@db.command()
def current():
    """ Downgrade database to a revision
    """
    alembic_command.current(alembic_config, verbose=True)

cli.add_command(db)


if __name__ == '__main__':
    cli()
