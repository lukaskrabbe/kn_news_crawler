# -*- coding: utf-8 -*-
import glob
import json
import os

from helpers.log import get_logger
from kn.prep import prep_kn_content

logger = get_logger("kn-data-prep")

if __name__ == "__main__":
    logger.info("Start Preparation of KN-Data")

    data_dir = "./data/prep/"
    if not os.path.exists(data_dir):
        logger.info("Create Data directory: %s" % data_dir)
        os.makedirs(data_dir)

    raw_data = [x[0] for x in os.walk("./data/raw/")]
    raw_data.remove("./data/raw/")
    raw_data = [x.split("/")[-1] for x in raw_data]
    prep_data = [x[0] for x in os.walk("./data/prep/")]
    prep_data.remove("./data/prep/")
    prep_data = [x.split("/")[-1] for x in prep_data]
    data_to_prep = list(set(raw_data) - set(prep_data))
    logger.info("Found %s folders (days) in raw folder to prepare", len(data_to_prep))

    for folder in ["./data/raw/" + x for x in data_to_prep]:
        logger.info("Start preparation of article data in %s", folder)

        if not os.path.exists(folder.replace("/raw/", "/prep/")):
            logger.info("Create Data directory: %s" % folder.replace("/raw/", "/prep/"))
            os.makedirs(folder.replace("/raw/", "/prep/"))

        for article_file in glob.glob(folder + "/*"):
            with open(article_file, "r") as json_file:
                data = json.load(json_file)
                prep_content = prep_kn_content(data)

            if len(prep_content["body"]) > 25 and prep_content["resort"] != "Rätsel":
                with open(article_file.replace("/raw/", "/prep/"), "w") as fp:
                    json.dump(prep_content, fp, indent=1, ensure_ascii=False)

    logger.info("Successfully prepared KN-Data")
