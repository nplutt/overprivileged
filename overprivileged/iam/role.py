from typing import List

from overprivileged.clients import fetch_boto3_client
from overprivileged.cloudwatch import run_query
from overprivileged.iam.action import create_action


def fetch_roles(path_prefix: str = "/", max_items: int = 200) -> List[dict]:
    """
    Fetches all of the iam roles for a given account
    Args:
        path_prefix: The path prefix for filtering the results
        max_items: The max number of roles to return
    """
    client = fetch_boto3_client("iam")

    res = client.list_roles(PathPrefix=path_prefix, MaxItems=max_items)
    return [
        {"name": r.get("RoleName"), "description": r.get("Description")}
        for r in res["Roles"]
    ]


def fetch_role_actions(role_name: str, log_group_name: str, days: int) -> dict:
    """
    Fetches all of the actions performed by an IAM role from a cloudtrail
    log group in cloudwatch.
    Args:
        role_name: the name of the role to search for actions by
        log_group_name: the name of the cloudwatch log group to search
        days: the number of days in the past that the log group should be searched
    """
    query = f"""
    fields 
        @timestamp as time, 
        eventName as name,
        eventSource as source,
        awsRegion as region
    | filter userIdentity.sessionContext.sessionIssuer.userName = '{role_name}'
    | count_distinct(concat(source, '-', name, '-', region)) as distinct_count 
        by source, name, region
    """
    results, query_cost = run_query(query, log_group_name, days)
    actions = sorted([create_action(r["source"], r["name"]) for r in results])
    return {
        "query_cost": query_cost,
        "actions": actions,
    }
