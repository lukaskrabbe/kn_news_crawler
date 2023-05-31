# -*- coding: utf-8 -*-
"""
KN-Data-DB-Upload

Loads Data from the MongoDB into Postgres DB kn.raw

Usage:
    kn_data_db_upload.py

Example:
    python kn_data_db_upload.py

Author: Lukas Krabbe (mail@l-krabbe.de)

Copyright (c) 2023 Lukas Krabbe
"""
import os
import sys

from helpers.db_connector import get_mongo_connection
from helpers.db_connector import get_posgtres_connection
from helpers.log import get_logger
from tqdm import tqdm

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

    # Get MongoDB Connection
    kn_collection = get_mongo_connection()

    # Extract all data from kn collection
    kn_data = list(kn_collection.find({}))

    # Get Postgres Connection
    conn = get_posgtres_connection()
    cur = conn.cursor()

    # Create Table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS raw.article_data (
            kn_id TEXT PRIMARY KEY,
            title TEXT,
            subtitle TEXT,
            authors TEXT,
            releaseDate DATE,
            city TEXT,
            resort TEXT,
            page INT,
            body TEXT,
            insert_timestamp TIMESTAMP DEFAULT NOW()
        )
    """
    )
    conn.commit()

    # Get ids of already inserted articles
    cur.execute(
        """
        SELECT kn_id FROM raw.article_data
    """
    )
    already_inserted = cur.fetchall()
    already_inserted = [x[0] for x in already_inserted]
    logger.info("Found %s already inserted articles" % len(already_inserted))

    # Filter out already inserted articles
    kn_data = list(kn_data)
    kn_data = [x for x in kn_data if x["id"] not in already_inserted]
    logger.info("Found %s new articles" % len(kn_data))

    # Insert Data
    for article in tqdm(kn_data):
        kn_id = article.get("id", None)
        subtitle = article.get("subtitle", None)
        city = article.get("city", None)
        resort = article.get("resort", None)
        title = article.get("title", None)
        authors = article.get("author", None)
        releaseDate = article.get("releaseDate", None)
        body = article.get("body", None)

        if authors is not None:
            authors = ""
            for author in article["author"].values():
                authors += author + ", "
            authors = authors[:-2]

        cur.execute(
            """
            INSERT INTO raw.article_data (
                kn_id,
                title,
                subtitle,
                authors,
                releaseDate,
                city,
                resort,
                body
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE (kn_id) DO NOTHING
        """,
            (kn_id, title, subtitle, authors, releaseDate, city, resort, body),
        )
        conn.commit()

    # Close Connection
    cur.close()
    conn.close()

    logger.info("Finished Upload of KN-Data to Postgres DB kn.raw")


if __name__ == "__main__":
    main(sys.argv)
