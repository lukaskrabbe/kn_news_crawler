# -*- coding: utf-8 -*-
"""
KN-Data-Consumer

This script downloads the KN-Data for a given date and stores it in a
local directory.

Usage:
    kn_data_consumer.py [-d <date>]

    -d, --date <date>   Date to download KN-Data for (default: today)

Example:
    python kn_data_consumer.py -d 01.01.2020

Author: Lukas Krabbe (mail@l-krabbe.de)

Copyright (c) 2020 Lukas Krabbe
"""
import argparse
import sys
from datetime import datetime

from helpers.log import get_logger
from helpers.secrets import get_secret_from_env
from kn.download import download

logger = get_logger("kn-data-consumer")


def parse_arguments(arguments: list):
    """
    Parse the arguments passed to the script

    Args:
        arguments (list): List of arguments passed to the script

    Returns:
        dict: Dictionary with the parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="KN-Data-Consumer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-d",
        "--date",
        type=str,
        default=datetime.today().strftime("%d.%m.%Y"),
        help="Date to download KN-Data for",
    )
    return parser.parse_args(arguments)


def main(arguments: list):
    """
    Main function for the KN-Data-Consumer

    Args:
        arguments (list): List of arguments passed to the script
    """
    args = parse_arguments(arguments)

    if args.date:
        load_date = datetime.strptime(args.date, "%d.%m.%Y")
    else:
        load_date = datetime.today()

    logger.info("Start KN-Download for %s", load_date.strftime("%d.%m.%Y"))

    secret = get_secret_from_env("KN_USER_SECRET")
    data_dir, article_data = download(load_date, secret)

    logger.info("KN-Data stored in %s", data_dir)
    logger.info("Successfully downloaded KN-Data")


if __name__ == "__main__":
    main(sys.argv[1:])
