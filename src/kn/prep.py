# -*- coding: utf-8 -*-
import re
from typing import Dict


CLEANR = re.compile("<.*?>")


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, "", raw_html)
    cleantext = cleantext.replace("&nbsp", " ")

    cleantext = cleantext.replace("\xa0", " ")
    cleantext = re.sub(r"\s", " ", cleantext)

    # doc = lxml.html.fromstring(raw_html)
    # cleaner = lxml.html.clean.Cleaner(style=True)
    # doc = cleaner.clean_html(doc)
    # cleantext = doc.text_content()

    return cleantext


def remove_von(value):
    return value.replace("Von ", "")


def remove_new_line(value):
    return value.replace("\xad", "").replace("\n", "")


def remove_multiple_spaces(value):
    return re.sub(" +", " ", value)


def prep_kn_content(raw_content_data: Dict[str, str]) -> Dict[str, str]:
    prep_content_data = {}

    for key, value in raw_content_data["content"].items():
        if type(value) == str:
            value = cleanhtml(value)
            value = remove_new_line(value)
            value = remove_multiple_spaces(value)
            if key == "author":
                value = remove_von(value)
            if key == "page":
                value = int(value)

        if key in [
            "author",
            "body",
            "title",
            "releaseDate",
            "page",
            "subtitle",
            "resort",
        ]:
            prep_content_data[key] = value

    return prep_content_data
