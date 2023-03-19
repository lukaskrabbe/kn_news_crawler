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

    try:
        with open(f"./secrets/{secret}.json", "r") as sv:
            secret_value = json.loads(sv.read())

        logger.info("Successfully load secret %s", secret)
        return secret_value
    except FileNotFoundError:
        logger.error(
            "Did not found secret %s in folder ./secrets/*",
            secret,
        )
        return None
