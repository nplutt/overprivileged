from typing import List

from src.clients import fetch_boto3_client


def fetch_iam_roles(path_prefix: str = "/", max_items: int = 200) -> List[dict]:
    """
    Fetches all of the iam roles for a given account
    Args:
        path_prefix: The path prefix for filtering the results
        max_items: The max number of roles to return
    """
    client = fetch_boto3_client("iam")

    res = client.list_roles(PathPrefix=path_prefix, MaxItems=max_items)
    return [
        {
            "arn": r["Arn"],
            "name": r.get("RoleName"),
            "description": r.get("Description"),
        }
        for r in res["Roles"]
    ]
