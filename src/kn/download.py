import requests
import re
import os
import json
import logging
from .login import login

logger = logging.getLogger("kn-download")


def _get_e_paper_id(session, date):
    url = "https://epaper.kieler-nachrichten.de/kieler-nachrichten/" + date
    response = session.request("GET", url)
    logger.info(
        "epaper.kieler-nachrichten/kieler-nachrichten - status code: %s"
        % response.status_code
    )
    assert response.status_code == 200

    current_id = re.findall(
        r"\d+", re.search('\/webreader\/[0-9]*" class', response.text).group()
    )[0]
    assert len(current_id) > 0, "Did not found an ID for e-paper!"
    logger.info("Found e-paper for %s, got id: %s", date, current_id)
    return current_id


def _get_e_paper_meta_data(session, current_id):
    url = "https://epaper.kieler-nachrichten.de/webreader-v3/config/" + current_id
    response = session.request("GET", url)
    logger.info(
        "epaper.kieler-nachrichten/webreader-v3 - status code: %s"
        % response.status_code
    )
    assert response.status_code == 200

    id = json.loads(response.text)["document"]["id"]
    assert len(str(id)) > 0, "Did not found an id for e-paper!"
    logger.info("Found e-paper-meta-data id: %s", id)

    articleViewDataUrl = json.loads(response.text)["document"]["articleViewDataUrl"]
    assert (
        len(str(articleViewDataUrl)) > 0
    ), "Did not found an articleViewDataUrl for e-paper!"
    logger.info("Found e-paper-meta-data articleViewDataUrl: %s", articleViewDataUrl)

    releaseDate = json.loads(response.text)["document"]["releaseDate"]
    assert len(str(releaseDate)) > 0, "Did not found an releaseDate for e-paper!"
    logger.info("Found e-paper-meta-data releaseDate: %s", releaseDate)

    title = json.loads(response.text)["document"]["title"]
    assert len(str(title)) > 0, "Did not found an title for e-paper!"
    logger.info("Found e-paper-meta-data title: %s", title)

    return {
        "id": id,
        "articleViewDataUrl": articleViewDataUrl,
        "releaseDate": releaseDate,
        "title": title,
    }


def _get_e_paper_article_view(session, articleViewDataUrl):
    url = (
        "https://epaper.kieler-nachrichten.de/webreader-v3/DataLoader.php?uri="
        + articleViewDataUrl
    )
    response = session.request("GET", url)
    logger.info(
        "epaper.kieler-nachrichten/webreader-v3/DataLoader - status code: %s"
        % response.status_code
    )
    assert response.status_code == 200

    article_data = json.loads(response.text)
    assert len(article_data) > 0, "No Data in article_view!"

    return article_data


def download(load_date, secret):
    """

    Args:
        load_date:
        secret:

    Returns:
        data_dir:
        article_data:
    """
    with requests.session() as session:
        assert login(session, secret), "Can not proceed due to unsuccessful login!"

        current_id = _get_e_paper_id(session, load_date.strftime("%d.%m.%Y"))
        meta_dict = _get_e_paper_meta_data(session, current_id)
        article_data = _get_e_paper_article_view(
            session, meta_dict["articleViewDataUrl"]
        )
        number_of_articles = sum([len(x) for x in article_data])
        logger.info(
            "Found %s pages with %s articles for %s",
            len(article_data),
            number_of_articles,
            load_date.strftime("%d.%m.%Y"),
        )

        data_dir = (
            "./data/raw/" + load_date.strftime("%d_%m_%Y") + "_" + current_id + "/"
        )
        if not os.path.exists(data_dir):
            logger.info("Create Data directory: %s" % data_dir)
            os.makedirs(data_dir)

        logger.info("Start writing article data to %s", data_dir)
        for page in range(1, len(article_data) + 1):
            logger.info(
                "Write article data of page %s/%s to file system",
                page,
                len(article_data),
            )
            for article in article_data[str(page)]:
                if article["media_type"] == "article_json":
                    article["epaper_meta_data"] = meta_dict
                    with open(data_dir + article["articleId"] + ".json", "w") as fp:
                        json.dump(article, fp, indent=1)
                    logger.debug(
                        "Successfully written article data in %s",
                        data_dir + article["articleId"] + ".json",
                    )

        check_sum = len(os.listdir(data_dir))
        assert check_sum > 0, "Did not write all articles to file system!"
        logger.info(
            "Successfully wrote %s files with article data to %s", check_sum, data_dir
        )
        return data_dir, article_data
