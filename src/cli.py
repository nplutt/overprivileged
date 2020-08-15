import json

import click

from src.exceptions import ClickException
from src.roles import fetch_iam_roles


@click.group()
@click.option("--region", help="The AWS region to run commands in")
def cli(region):
    pass


@cli.command("list-roles", help="List IAM role names for the current AWS account")
@click.option(
    "--path-prefix",
    help="Filter IAM roles based off of a given path prefix",
    default="/",
)
@click.option("--max-items", help="The max number of roles to return", default=200)
def list_roles(path_prefix, max_items) -> None:
    roles = fetch_iam_roles(path_prefix, max_items)
    click.echo(json.dumps(roles, sort_keys=True, indent=4))


@cli.command("check-privileges")
@click.option(
    "--role-arn', help='The ARN of the role for who's privileges should be checked"
)
def check_privileges() -> None:
    click.echo("Test...")


def main() -> None:
    try:
        cli()
    except ClickException as e:
        print(e)
