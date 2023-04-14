# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime

from log_utils.helper import LogHelper
from pytz import timezone


def get_logger(function: str):
    """Get Logger for function

    Args:
        function: Name of the function

    Returns:
        logger: Logger for function
    """
    log_dir = f"./data/logs/{datetime.today().strftime('%d_%m_%Y')}/"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    def time_tz(*args):
        return datetime.now(tz).timetuple()

    tz = timezone("Europe/Berlin")

    logging.Formatter.converter = time_tz
    logging.basicConfig(
        filename=log_dir + function + ".log",
        filemode="w",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )

    logger = logging.getLogger()
    logger.addHandler(LogHelper.generate_color_handler())
    logger.setLevel(logging.INFO)

    return logger
