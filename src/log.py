import os
import logging
from pytz import timezone
from datetime import datetime
from log_utils.helper import LogHelper


def get_logger(function: str):
    """

    Args:
        function:

    Returns:
        logger: Logger
    """
    log_dir = "../data/logs/"
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
