import click

from chicky import __version__


@click.command()
@click.pass_context
def version_command(context):
    """
    Print out version information.
    """
    click.echo("chicky {}".format(__version__))
