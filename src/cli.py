import json

import click

from src.cloudwatch import fetch_role_iam_actions
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
def list_roles(path_prefix: str, max_items: int) -> None:
    roles = fetch_iam_roles(path_prefix, max_items)
    click.echo(json.dumps(roles, sort_keys=True, indent=4))


@cli.command("check-privileges")
@click.option(
    "--role-arn", help="The ARN of the role for who's privileges should be checked.",
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
def check_privileges(role_arn: str, log_group_name: str, days: int) -> None:
    actions = fetch_role_iam_actions(role_arn, log_group_name, days)
    click.echo(json.dumps(actions, sort_keys=True, indent=4))


def main() -> None:
    try:
        cli()
    except ClickException as e:
        print(e)
