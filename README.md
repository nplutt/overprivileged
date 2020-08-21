# overprivileged
Overprivileged is a utility for discovering over privileged IAM roles in AWS. 

**Caution:** This software is in version 0.0.1 and not currently tested

## Installation
From PyPi:
```bash
$ pip install overprivileged
```

## Usage
Overprivileged utilizes Cloudtrail logs stored in Cloudwatch to parse out exactly which IAM actions
have been performed by an IAM role over a given number of days and returns a diff of which IAM actions
have been used and which ones have not.

### Prerequisites
1. Cloudtrail logging enabled
2. Cloudtrail logs saved to Cloudwatch log group

### CLI

**Check Role Privileges**

Example Usage:
```bash
op check-privileges \
    --role-name role-name \
    --log-group-name cloudtrail-log-group-name \
    --days 5
```

Example Output:
```json
{
    "usedActions": [
        "route53:ListHostedZones",
        "route53:ListResourceRecordSets"
    ],
    "unusedActions": [
        "route53:ChangeResourceRecordSets"
    ]
}
```

Help:
```bash
op check-privileges --help
Usage: op check-privileges [OPTIONS]

  Checks what actions are used and unused by a role

Options:
  --role-name TEXT       The name of the role to check privileges for.
  --log-group-name TEXT  The name of the log group where the Cloudtrail logs
                         are stored.

  --days INTEGER RANGE   The number of days in the past that the current
                         privileges should be checked against.

  --region TEXT          The aws region where the log group is stored.
  --help                 Show this message and exit.
```
