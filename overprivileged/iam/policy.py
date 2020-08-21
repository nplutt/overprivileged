from typing import List

from overprivileged.clients import fetch_boto3_client
from overprivileged.iam.action import load_all_possible_actions_from_action


def fetch_policy_actions_for_role(role_name: str) -> List[str]:
    """
    Loads all of the iam actions listed in a given role's policies
    Args:
        role_name: the name of the role to fetch iam actions for
    """
    policies = fetch_role_policies(role_name)

    actions = set()
    for policy in policies.values():
        actions.update(fetch_actions_from_policy(policy))

    return sorted(list(actions))


def fetch_explicit_policy_actions_for_role(role_name: str) -> List[str]:
    """
    Loads all of the explicit iam actions listed in a given role's policies
    Args:
        role_name: the name of the role to fetch explicit iam actions for
    """
    actions = fetch_policy_actions_for_role(role_name)

    explicit_actions = set()
    for action in actions:
        explicit_actions.update(load_all_possible_actions_from_action(action))

    return sorted(list(explicit_actions))


def fetch_role_policies(role_name: str) -> dict:
    inline_policies = fetch_inline_policies_for_role(role_name)
    attached_policies = fetch_attached_policies_for_role(role_name)
    return {**inline_policies, **attached_policies}


def fetch_inline_policies_for_role(role_name: str) -> dict:
    client = fetch_boto3_client("iam")

    policy_documents = {}
    inline_role_policies = client.list_role_policies(RoleName=role_name)
    for policy_name in inline_role_policies["PolicyNames"]:
        policy = client.get_role_policy(RoleName=role_name, PolicyName=policy_name)
        policy_documents[policy_name] = policy["PolicyDocument"]

    return policy_documents


def fetch_attached_policies_for_role(role_name: str) -> dict:
    client = fetch_boto3_client("iam")

    policy_documents = {}
    attached_role_policies = client.list_attached_role_policies(RoleName=role_name)
    for policy_info in attached_role_policies["AttachedPolicies"]:
        policy_arn = policy_info["PolicyArn"]
        policy = client.get_policy_version(
            PolicyArn=policy_arn, VersionId=fetch_version_for_policy(policy_arn),
        )
        policy_documents[policy_info["PolicyName"]] = policy["PolicyVersion"][
            "Document"
        ]

    return policy_documents


def fetch_version_for_policy(policy_arn: str) -> str:
    client = fetch_boto3_client("iam")
    policy = client.get_policy(PolicyArn=policy_arn)
    return policy["Policy"]["DefaultVersionId"]


def fetch_actions_from_policy(policy: dict) -> List[str]:
    actions = set()
    for block in policy["Statement"]:
        actions.update(block["Action"])

    return list(actions)
