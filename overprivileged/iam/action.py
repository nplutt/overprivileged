import re
from typing import List

from overprivileged.static.iam_actions import actions


prefix_overrides = {
    "tagging": "tag",
}


def create_action(source: str, name: str) -> str:
    prefix = source.split(".")[0]
    prefix = prefix_overrides.get(prefix, prefix)
    return f"{prefix}:{name}"


def load_all_possible_actions_from_action(action: str) -> List[str]:
    action = action.replace("*", ".*")

    parts = action.split(":")
    prefix = parts[0]
    action = "".join(parts[1:])

    prefix_filter = re.compile(f"^{prefix}")
    action_filter = re.compile(f"^{action}")

    matched = []
    matched_prefixes = list(filter(prefix_filter.fullmatch, actions.keys()))
    for mp in matched_prefixes:
        matched_actions = list(filter(action_filter.fullmatch, actions[mp]))
        matched.extend([f"{mp}:{ma}" for ma in matched_actions])

    return matched
