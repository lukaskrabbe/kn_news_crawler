"""
    Module used to play Around
"""
import os
import logging
from pytz import timezone
from datetime import datetime
from log_utils.helper import LogHelper
from typing import Optional

log_dir = "../data/logs/"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def time_tz(*args):
    return datetime.now(tz).timetuple()


tz = timezone("Europe/Berlin")

logging.Formatter.converter = time_tz
logging.basicConfig(
    filename=log_dir + "string_function.log",
    filemode="w",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger()
logger.addHandler(LogHelper.generate_color_handler())
logger.setLevel(logging.INFO)


def double_string(text: str) -> str:
    """
    Function to double a given input String

    Args:
        text: String to double

    Returns:
        value: Value which contains the doubled String
    """
    value = text * 2
    return value


def write_string_to_file(
    text: str, file_name: str, data_dir: Optional[str] = "./../data/raw/"
) -> str:
    """Function

    Args:
        text: String which will be written to File
        file_name: Filename
        data_dir: Optional data path

    Returns:
        file_path: Path to the created file

    """
    if not os.path.exists(data_dir):
        logger.info("Create Data directory: %s" % data_dir + file_name)
        os.makedirs(data_dir)

    with open(data_dir + file_name, "w") as text_file:
        logger.info("Write file %s" % data_dir + file_name)
        text_file.write(text)

    return data_dir + file_name


if __name__ == "__main__":
    write_string_to_file("Hallo Welt", "test.txt")
