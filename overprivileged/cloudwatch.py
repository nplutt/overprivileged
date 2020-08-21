from datetime import datetime, timedelta
from decimal import Decimal, getcontext
from enum import Enum
from time import mktime, sleep, time
from typing import List, Tuple

from overprivileged.clients import fetch_boto3_client


class QueryStatus(Enum):
    COMPLETE = "Complete"
    FAILED = "Failed"


def run_query(
    query: str, log_group_name: str, days: int, timeout_min: int = 5
) -> Tuple[List[dict], Decimal]:
    """
    Runs a query against a given log group name via Cloudwatch insights
    Args:
        query: the query to be run
        log_group_name: the log group to run the query against
        days: the number of days back to query
        timeout_min: the number of minutes before the query should be canceled
    """
    timeout = datetime.utcnow() + timedelta(minutes=timeout_min)
    query_id = start_query(query, log_group_name, days)
    return fetch_query_results(query_id, timeout)


def start_query(query: str, log_group_name: str, days: int) -> str:
    """
    Starts a cloudwatch insights query
    Args:
        query: the query to be run
        log_group_name: the log group to run the query against
        days: the number of days back to query
    """
    client = fetch_boto3_client("logs")

    start_time = mktime((datetime.utcnow() - timedelta(days=days)).timetuple())
    end_time = time()

    query_response = client.start_query(
        logGroupName=log_group_name,
        startTime=round(start_time),
        endTime=round(end_time),
        queryString=query,
        limit=10000,
    )
    return query_response["queryId"]


def fetch_query_results(query_id: str, timeout: datetime) -> Tuple[List[dict], Decimal]:
    """
    Waits for and returns the results from a given cloudwatch insights
    query
    Args:
        query_id: the query id to fetch results for
        timeout: the time at which the query should be canceled/timed out
    """
    client = fetch_boto3_client("logs")

    results = None
    while datetime.utcnow() < timeout:
        sleep(2)
        results = client.get_query_results(queryId=query_id)
        if results["status"] in [
            QueryStatus.COMPLETE.value,
            QueryStatus.FAILED.value,
        ]:
            break

    query_price = calculate_query_price(results["statistics"]["bytesScanned"])
    results = [
        {r["field"]: r["value"] for r in records} for records in results["results"]
    ]
    return results, query_price


def calculate_query_price(bytes_scanned: int) -> Decimal:
    """
    Takes the number of bytes scanned during a query and returns the price
    AWS will charge for running the query
    Args:
         bytes_scanned: number of bytes scanned during the query
    """
    getcontext().prec = 2
    gigabytes_scanned = Decimal(bytes_scanned) * Decimal(0.000000001)
    return gigabytes_scanned * Decimal(0.005)
