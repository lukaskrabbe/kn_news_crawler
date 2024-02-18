# -*- coding: utf-8 -*-
"""
KN-Data-Upload

Step 3: Upload KN-Data to MongoDB

This script uploads the prepared KN-Data to a MongoDB.

Usage:
    kn_data_upload.py

Example:
    python kn_data_upload.py

Author: Lukas Krabbe (mail@l-krabbe.de)

Copyright (c) 2023 Lukas Krabbe
"""
import glob
import json
import os
import sys

import pymongo
from helpers.log import get_logger
from helpers.secrets import get_secret_from_env

logger = get_logger("kn-data-upload")


def main(param: list):
    """
    Main function for the KN-Data-Upload

    Args:
        param: List of arguments passed to the script

    Returns:

    """
    logger.info("Start Upload of KN-Data")

    secret = get_secret_from_env("MONGO_USER_SECRET")

    client = pymongo.MongoClient(
        f"mongodb://{secret['user']}:{secret['password']}@81.169.252.177:27017/?authMechanism=DEFAULT&tls=false"
    )
    kn_db = client.kn_db
    kn_collection = kn_db.get_collection("kn_data")
    # kn_collection.delete_many({})

    prep_data = [x[0] for x in os.walk("./data/prep/")]
    prep_data.remove("./data/prep/")
    prep_data = [x.split("/")[-1] for x in prep_data]

    for folder in ["./data/prep/" + x for x in prep_data]:
        files = glob.glob(folder + "/*")
        logger.info("Start to upload %s files from %s", len(files), folder)

        exists = 0
        for article_file in glob.glob(folder + "/*"):
            with open(article_file) as f:
                file_data = json.load(f)
                file_data["id"] = article_file.split("/")[-1].split(".")[0]
                if not len(list(kn_collection.find({"id": file_data["id"]}))) != 0:
                    kn_collection.insert_one(file_data)
                else:
                    exists += 1

        logger.info("Inserted %s Documents into DB", len(files) - exists)


if __name__ == "__main__":
    main(sys.argv)
