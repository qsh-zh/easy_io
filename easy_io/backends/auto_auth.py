import contextlib
import json
from typing import Any, Optional

from easy_io import log

CRED_ENVS = None
CRED_ENVS_DICT = None

DEPLOYMENT_ENVS = ["prod", "dev", "stg"]


# context manger to open a file or read from env variable
@contextlib.contextmanager
def open_auth(s3_credential_path: Optional[Any], mode: str):
    if not s3_credential_path:
        log.info(f"No credential file provided {s3_credential_path}.")
        yield None
        return

    name = s3_credential_path.split("/")[-1].split(".")[0]
    if not name:
        raise ValueError(f"Could not parse into env var: {s3_credential_path}")
    cred_env_name = f"PROD_{name.upper()}"

    if CRED_ENVS.APP_ENV in DEPLOYMENT_ENVS and cred_env_name in CRED_ENVS_DICT:
        object_storage_config = get_creds_from_env(cred_env_name)
        log.info(f"using ENV vars for {cred_env_name}")

        yield object_storage_config
    else:
        log.info(f"using credential file: {s3_credential_path}")
        with open(s3_credential_path, mode) as f:
            yield f


def get_creds_from_env(cred_env_name: str) -> dict[str, str]:
    try:
        object_storage_config = CRED_ENVS_DICT[cred_env_name]
    except KeyError as error:
        raise ValueError(f"Could not find {cred_env_name} in CRED_ENVS") from error
    empty_args = {key.upper() for key in object_storage_config if object_storage_config[key] == ""}
    if empty_args:
        raise ValueError(f"Some required environment variable(s) were not provided for {cred_env_name}", empty_args)
    return object_storage_config


def json_load_auth(f):
    if CRED_ENVS.APP_ENV in DEPLOYMENT_ENVS:
        return f if f else {}
    else:
        return json.load(f)
