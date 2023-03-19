# -*- coding: utf-8 -*-
from datetime import datetime

from helpers.log import get_logger
from helpers.secrets import get_secret_from_env
from kn.download import download

logger = get_logger("kn-data-consumer")

if __name__ == "__main__":
    load_date = datetime.today()
    logger.info("Start KN-Download for %s", load_date.strftime("%d.%m.%Y"))

    secret = get_secret_from_env("KN_USER_SECRET")
    data_dir, article_data = download(load_date, secret)

    logger.info("Successfully downloaded KN-Data")
