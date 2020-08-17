import json

import click

from overprivileged.iam.policy import fetch_role_policy_actions
from overprivileged.iam.role import fetch_role_actions, fetch_roles


@click.group()
def cli():
    pass


@cli.command("list-roles", help="List IAM role names for the current AWS account")
@click.option(
    "--path-prefix",
    help="Filter IAM roles based off of a given path prefix",
    type=click.STRING,
    default="/",
)
@click.option(
    "--max-items",
    help="The max number of roles to return",
    type=click.INT,
    default=200,
)
def list_roles(path_prefix: str, max_items: int) -> None:
    roles = fetch_roles(path_prefix, max_items)
    click.echo(json.dumps(roles, sort_keys=True, indent=4))


@cli.command(
    "list-role-actions", help="List all IAM actions that can be performed by a role"
)
@click.option(
    "--role-name",
    help="The name of the role for who's actions should be listed",
    type=click.STRING,
)
def list_role_actions(role_name: str) -> None:
    actions = fetch_role_policy_actions(role_name)
    click.echo(json.dumps(actions, sort_keys=True, indent=4))


@cli.command("check-privileges")
@click.option(
    "--role-name",
    help="The name of the role for who's privileges should be checked.",
    type=click.STRING,
)
@click.option(
    "--log-group-name",
    help="The name of the log group where the Cloudtrail logs are stored.",
    type=click.STRING,
)
@click.option(
    "--days",
    help="The number of days in the past that the current privileges should be "
    "checked against.",
    type=click.IntRange(1, 15),
    default=3,
)
@click.option(
    "--region",
    help="The aws region where the log group is stored.",
    type=click.STRING,
    default=None,
)
def check_privileges(
    role_name: str, log_group_name: str, days: int, region: str = None
) -> None:
    actions = fetch_role_actions(role_name, log_group_name, days)
    click.echo(json.dumps(actions, sort_keys=True, indent=4))

    actions = fetch_role_policy_actions(role_name)
    click.echo(json.dumps(actions, sort_keys=True, indent=4))


def main() -> None:
    cli()
