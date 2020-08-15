from collections import defaultdict
from datetime import datetime, timedelta
from enum import Enum
from time import mktime, sleep, time
from typing import Dict, List

from src.clients import fetch_boto3_client


class QueryStatus(Enum):
    COMPLETE = "Complete"
    FAILED = "Failed"
    RUNNING = "Running"
    SCHEDULED = "Scheduled"


def fetch_role_iam_actions(
    role_arn: str, log_group_name: str, days: int,
):
    """
    Fetches all of the actions performed by an IAM role
    from a cloudtrail log stored in cloudwatch.
    Args:
        role_arn: the arn of the role to search for actions by
        log_group_name: the name of the cloudwatch log group to search
        days: the number of days in the past that the log group should be searched
    """
    query_timeout = datetime.utcnow() + timedelta(minutes=5)
    query_id = start_query(role_arn, log_group_name, days)
    results = fetch_query_results(query_id, query_timeout)
    return build_unique_actions(results)


def start_query(role_arn: str, log_group_name: str, days: int,) -> str:
    client = fetch_boto3_client("logs")

    start_time = mktime((datetime.utcnow() - timedelta(days=days)).timetuple())
    end_time = time()

    query = f"""
        fields @timestamp as time, eventName as name, eventSource as source, awsRegion as region
        | filter userIdentity.sessionContext.sessionIssuer.arn = '{role_arn}'
        | sort @timestamp desc
        """
    query_response = client.start_query(
        logGroupName=log_group_name,
        startTime=round(start_time),
        endTime=round(end_time),
        queryString=query,
        limit=10000,
    )
    return query_response["queryId"]


def fetch_query_results(query_id: str, timeout: datetime) -> List[dict]:
    client = fetch_boto3_client("logs")

    results = None
    while datetime.utcnow() < timeout:
        sleep(5)
        results = client.get_query_results(queryId=query_id)
        if results["status"] in [
            QueryStatus.COMPLETE.value,
            QueryStatus.FAILED.value,
        ]:
            break

    return [{r["field"]: r["value"] for r in records} for records in results["results"]]


def build_unique_actions(results: dict) -> Dict[str, list]:
    actions = defaultdict(set)

    for r in results:
        source = r["source"].split(".")[0]
        actions[source].add(r["name"])

    return {k: list(v) for k, v in actions.items()}
