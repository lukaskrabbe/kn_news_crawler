# -*- coding: utf-8 -*-
import json
import logging
from typing import Dict
from typing import Optional

logger = logging.getLogger("secrets")


def get_secret_from_env(
    secret: str, path: Optional[str] = "./secrets/"
) -> Dict[str, str]:
    """

    Args:
        path:
        secret:

    Returns:
        secret_value: None if Secret does not exists, dict if exists
    """

    try:
        with open(f"{path}{secret}.json", "r") as sv:
            secret_value = json.loads(sv.read())

        logger.info("Successfully load secret %s", secret)
        return secret_value
    except FileNotFoundError:
        logger.error(
            "Did not found secret %s in folder %s",
            secret,
            path,
        )
        return None
