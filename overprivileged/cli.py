import json

import click

from overprivileged.exceptions import ClickException
from overprivileged.iam.role import fetch_role_actions, fetch_roles
from overprivileged.iam.policy import fetch_role_policies


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
def list_roles(path_prefix: str, max_items: int) -> None:
    roles = fetch_roles(path_prefix, max_items)
    click.echo(json.dumps(roles, sort_keys=True, indent=4))


@cli.command("check-privileges")
@click.option(
    "--role-name", help="The name of the role for who's privileges should be checked.",
)
@click.option(
    "--log-group-name",
    help="The name of the log group where the Cloudtrail logs are stored.",
)
@click.option(
    "--days",
    help="The number of days in the past that the current privileges should be "
    "checked against.",
    default=14,
)
def check_privileges(role_name: str, log_group_name: str, days: int) -> None:
    # actions = fetch_role_actions(role_name, log_group_name, days)
    policies = fetch_role_policies(role_name)
    click.echo(json.dumps(policies, sort_keys=True, indent=4))


def main() -> None:
    try:
        cli()
    except ClickException as e:
        print(e)
