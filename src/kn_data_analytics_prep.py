# -*- coding: utf-8 -*-
"""
KN-Data-Analytics-Prep

This script prepares the KN-Data for further Analytics.

Usage:
    kn_data_analytics_prep.py

Example:
    python kn_data_analytics_prep.py

Author: Lukas Krabbe (mail@l-krabbe.de)

Copyright (c) 2023 Lukas Krabbe
"""
import os
import sys

import pymongo
from helpers.analytics_prep import clean_articles
from helpers.analytics_prep import export_words
from helpers.analytics_prep import prep_authors
from helpers.analytics_prep import stop_words
from helpers.log import get_logger
from helpers.secrets import get_secret_from_env

logger = get_logger("kn-data-analytics-prep")


def main(param: list):
    """
    Main function for the KN-Data-Upload

    Args:
        param: List of arguments passed to the script

    Returns:

    """
    logger.info("Start Analytics-Preparation of KN-Data")

    data_dir = "../data/analytics/"
    if not os.path.exists(data_dir):
        logger.info("Create Data directory: %s" % data_dir)
        os.makedirs(data_dir)

    secret = get_secret_from_env("MONGO_USER_SECRET", path="../secrets/")

    client = pymongo.MongoClient(
        f"mongodb://{secret['user']}:{secret['password']}@81.169.252.177:27017/?authMechanism=DEFAULT&tls=false"
    )
    kn_db = client.kn_db
    kn_collection = kn_db.get_collection("kn_data")

    assert len(kn_collection.find_one({})) > 0, "Error, no Data or DB-Connection"

    prep_authors(kn_collection, data_dir + "authors.json")
    words = export_words(kn_collection, data_dir + "words.json")
    stop_words_df = stop_words(words, data_dir + "stop_words.csv")
    clean_articles(kn_collection, stop_words_df)

    logger.info("Finished Analytics-Preparation of KN-Data")


if __name__ == "__main__":
    main(sys.argv)
