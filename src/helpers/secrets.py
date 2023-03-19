import os
import json
import logging
from typing import Dict

logger = logging.getLogger("secrets")


def get_secret_from_env(secret: str) -> Dict[str, str]:
    """

    Args:
        secret:

    Returns:
        secret_value: None if Secret does not exists, dict if exists
    """
    if secret in os.environ:
        secret_value = os.environ[secret]
        secret_value = json.loads(secret_value)
    else:
        logger.error("Did not found secret %s in os env", secret)
        return None

    if "user" in secret_value and "password" in secret_value:
        logger.info("Successfully load secret %s", secret)
        return secret_value
    else:
        logger.warn("Dit not found user and password in secret %s", secret)
        return None
