# pydantic-kms-secrets
[![PyPI version](https://badge.fury.io/py/pydantic-kms-secrets.svg)](https://badge.fury.io/py/pydantic-kms-secrets)
![Upload Python Package](https://github.com/nplutt/pydantic-kms-secrets/workflows/Upload%20Python%20Package/badge.svg)

Utility to decrypt and encrypt secrets using [AWS KMS keys](https://aws.amazon.com/kms/) 
that also integrates with [pydantic](https://pydantic-docs.helpmanual.io/) models which allows for
encrypted values to be stored in `.env` files and be decrypted at runtime.

## Installation
From PyPi:
```bash
$ pip install pydantic-kms-secrets
```

## Usage

### CLI
Encrypt a secret:
```bash
$ pks -k your-kms-key-id -v my-secret-password -e
```

Decrypt a secret:
```bash
$ pks -k your-kms-key-id -v your-encrypted-secret -d
```

Help docs:
```bash
$ pks --help
usage: pks [-h] [-k KEY_ID] -v VALUE [-e] [-d]

Tool to encrypt and decrypt secrets via a KMS key

optional arguments:
  -h, --help            show this help message and exit
  -k KEY_ID, --key-id KEY_ID
                        ID of the KMS key to use
  -v VALUE, --value VALUE
                        The value to be encrypted
  -e, --encrypt         Set to encrypt value
  -d, --decrypt         Set to decrypt value
```

### Pydantic
Pydantic KMS Secrets is able to integrate and add functionality on top of Pydantic's 
[dotenv extension](https://pydantic-docs.helpmanual.io/usage/settings/) by allowing you
to store encrypted values in your `.env` files and decrypt them at runtime. A basic implementation
would look something like: 

**Pydantic Settings Model**
```python
from pydantic import BaseSettings
from src import KMSSecretStr, decrypt_kms_secrets


class Settings(BaseSettings):
    env: str
    secrets_kms_key_id: str  # This model attribute must exist to decrypt secrets
    kms_secret_1: KMSSecretStr
    kms_secret_2: KMSSecretStr

    class Config:
        env_file = ".env"

# Don't forget to call decrypt_kms_secrets, if you don't the secrets will not be decrypted
settings = decrypt_kms_secrets(Settings())
```

**`.env` File**
```bash
ENV="prod"

SECRETS_KMS_KEY_ID="your-kms-key-id"  # This environment variable must be set to decrypt secrets
KMS_SECRET_1="my-first-encrypted-secret"
KMS_SECRET_2="my-second-encrypted-secret"
```

**KMSSecretStr** Class

The `KMSSecretStr` class is almost identical to the [SecretStr](https://pydantic-docs.helpmanual.io/usage/types/#secret-types)
type in pydantic. 
```python
# This example uses the settings value from the python example above

# Standard access methods will not display the secret
print(settings)
#> env='prod' secrets_kms_key_id='your-kms-key-id' kms_secret_1=KMSSecretStr('**********') kms_secret_2=KMSSecretStr('**********')
print(settings.kms_secret_1)
#> **********
print(settings.dict())
"""
{
    'env': 'prod',
    'secret_kms_key_id': 'your-kms-key-id',
    'kms_secret_1': KMSSecretStr('**********'),
    'kms_secret_2': KMSSecretStr('**********'),
}
"""
print(settings.json())
#> {"env": "prod", "secret_kms_key_id": "your-kms-key-id", "kms_secret_1": "**********", "kms_secret_2": "**********"}

# Use get_secret_value method to see the secret's content.
print(settings.kms_secret_1.get_secret_value())
#> my-first-encrypted-secret
print(settings.kms_secret_2.get_secret_value())
#> my-second-encrypted-secret
```
 

