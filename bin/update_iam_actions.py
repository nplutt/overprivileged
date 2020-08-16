import json

import requests


if __name__ == "__main__":
    res = requests.get(
        "https://raw.githubusercontent.com/witoff/aws-iam-reference/master/reference.json"
    )
    service_map = res.json()["serviceMap"]

    iam_actions = {}
    for service_name in service_map:
        service = service_map[service_name]
        iam_actions[service["StringPrefix"]] = service["Actions"]

    actions_file = open("./src/iam/actions.py", "w")
    actions_file.write(f"actions = {json.dumps(iam_actions, indent=4)}")
    actions_file.close()
