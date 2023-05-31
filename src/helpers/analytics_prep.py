# -*- coding: utf-8 -*-
import json
import os
import re
from typing import Any
from typing import Dict

import nltk
import numpy as np
import pandas as pd
import pymongo
from HanTa import HanoverTagger as ht
from helpers.constants import REMOVE_WORDS
from helpers.log import get_logger
from kneed import KneeLocator
from tqdm import tqdm

logger = get_logger("kn-data-analytics-prep-analytics_prep")


def prep_authors(
    kn_collection: pymongo.collection.Collection, json_path: str
) -> Dict[str, Dict[str, Any]]:
    """
    Prepares the authors for further processing

    Args:
        kn_collection: Collection of the KN-Data
        json_path: Path to store the authors

    Returns:
        authors: Dict of authors
    """
    logger.info("Start to prepare authors")

    authors = {}
    for article in kn_collection.find():
        if "author" not in article:
            continue

        for author, author_name in article["author"].items():
            if author_name not in authors:
                authors[author_name] = {"name": author_name, "articles": []}
            article_dict = {
                "title": article.get("title", None),
                "date": article.get("releaseDate", None),
                "city": article.get("city", None),
                "resort": article.get("resort", None),
                "id": article.get("id", None),
            }
            authors[author_name]["articles"].append(article_dict)

    for author in authors.values():
        author["article_count"] = len(author["articles"])

        cities = {}
        for article in author["articles"]:
            if article["city"] not in cities:
                cities[article["city"]] = 0
            cities[article["city"]] += 1
        author["top_city"] = max(cities, key=cities.get)
        author["top_city_count"] = cities[author["top_city"]]

        resorts = {}
        for article in author["articles"]:
            if article["resort"] not in resorts:
                resorts[article["resort"]] = 0
            resorts[article["resort"]] += 1
        author["top_resort"] = max(resorts, key=resorts.get)
        author["top_resort_count"] = resorts[author["top_resort"]]

    with open(json_path, "w") as authors_file:
        json.dump(authors, authors_file)

    logger.info("Successfully prepared authors, found %s authors", len(authors))
    return authors


def _tokenize(text):
    # first tokenize by sentence, then by word to ensure that
    # punctuation is caught as it's own token
    tokens = [
        word.lower()
        for sent in nltk.sent_tokenize(text)
        for word in nltk.word_tokenize(sent)
    ]
    filtered_tokens = []
    # filter out any tokens not containing letters
    # (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search("[a-zA-Z]", token):
            filtered_tokens.append(token)
    return filtered_tokens


def stop_words(words: Dict[str, Dict[str, Any]], csv_path: str) -> pd.DataFrame:
    """
    Detects the stop words from the words in dict
    Args:
        words: Dict of words, format:
            {
                "word": {
                    "count": 1,
                    "ground_word": "word",
                    "word_art": "NN"
                    "article_count": 1
                }
            }

    Returns:
        df: DataFrame with stop words

    """
    df = pd.DataFrame(words).T
    df = df.reset_index(drop=True)
    df = df.sort_values("count", ascending=False)
    df = df.reset_index(drop=True)
    kn = KneeLocator(
        df.index, df["count"], S=2.5, curve="convex", direction="decreasing"
    )
    df["stop_word"] = np.where(df.index <= kn.knee, True, False)
    logger.info(
        f"Summe von Stop Words: {len(df[df['stop_word']])}/{len(df)} "
        f"({round(len(df[df['stop_word']])/len(df), 2)} %)"
    )
    logger.info(
        f"Vorkommen von Stop Words: "
        f"{df[df['stop_word'] is True]['count'].sum()}/{df['count'].sum()} "
        f"({round(df[df['stop_word'] is True]['count'].sum()/df['count'].sum(), 2)} %)"
    )

    df.to_csv(csv_path, index=False)

    return df


def export_words(
    kn_collection: pymongo.collection.Collection, json_path: str
) -> Dict[str, Dict[str, Any]]:
    """
    Prepares the words for further processing

    Args:
        kn_collection: Collection of the KN-Data
        json_path: Path to store the articles

    Returns:
        articles: Dict of articles
    """
    if json_path.endswith(".json") is not True:
        raise ValueError("json_path must end with .json")

    if os.path.exists(json_path) is True:
        return json.load(open(json_path, "r"))

    logger.info("Start to prepare articles")

    tagger = ht.HanoverTagger("morphmodel_ger.pgz")
    nltk.download("stopwords")

    words = {}
    data = list(kn_collection.find())
    for article in tqdm(data):
        lemmata = tagger.tag_sent(_tokenize(article["body"]), taglevel=1)

        for word, ground_word, word_art in lemmata:
            if word_art in ["NE"]:
                word = word.lower()
            else:
                word = ground_word.lower()

            if word in REMOVE_WORDS:
                continue

            if len(word) > 1 and not word.startswith("www") and word.isalpha():
                if word not in words:
                    words[word] = {
                        "word": word,
                        "word_art": word_art,
                        "count": 0,
                        "articles": [],
                    }

                words[word]["count"] += 1
                if article["id"] not in words[word]["articles"]:
                    words[word]["articles"].append(article["id"])

    for word in words:
        words[word]["article_count"] = len(words[word]["articles"])
        del words[word]["articles"]

    with open(json_path, "w") as words_file:
        json.dump(words, words_file)

    logger.info("Successfully prepared articles, found %s articles", len(words))
    return words


def clean_articles(kn_collection, stop_words):
    """
    Cleans the articles, removes stop words, etc.

    Args:
        kn_collection:
        data_dir:
        stop_words:

    Returns:

    """
    logger.info("Start to prepare articles")

    tagger = ht.HanoverTagger("morphmodel_ger.pgz")
    nltk.download("stopwords")
    # get stop words where stop_word is true
    stop_words = stop_words[stop_words["stop_word"] is True]["word"].tolist()

    data = list(kn_collection.find())
    for article in tqdm(data):
        if "body_clean" in article:
            continue

        lemmata = tagger.tag_sent(_tokenize(article["body"]), taglevel=1)

        body = []
        for word, ground_word, word_art in lemmata:
            if word_art in ["NE"]:
                word = word.lower()
            else:
                word = ground_word.lower()

            if word in REMOVE_WORDS:
                continue

            if word in stop_words:
                continue

            if len(word) > 1 and not word.startswith("www") and word.isalpha():
                body.append(word)

        kn_collection.update_one(
            {"_id": article["_id"]}, {"$set": {"body_clean": " ".join(body)}}
        )
        article["body_clean"] = " ".join(body)

    logger.info("Successfully prepared articles")
    return data
