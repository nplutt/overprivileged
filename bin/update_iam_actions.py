import json
from collections import defaultdict

import requests


if __name__ == "__main__":
    res = requests.get(
        "https://raw.githubusercontent.com/witoff/aws-iam-reference/master/reference.json"
    )
    service_map = res.json()["serviceMap"]

    iam_actions = defaultdict(set)
    for service_name in service_map:
        service = service_map[service_name]
        iam_actions[service["StringPrefix"]].update(service["Actions"])

    for k, v in iam_actions.items():
        iam_actions[k] = sorted(list(v))

    actions_file = open("./overprivileged/static/iam_actions.py", "w")
    actions_file.write(f"actions = {json.dumps(iam_actions, indent=4)}")
    actions_file.close()
