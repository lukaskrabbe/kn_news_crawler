# -*- coding: utf-8 -*-
import re
from typing import Dict

CLEANR = re.compile("<.*?>")


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, "", raw_html)
    cleantext = cleantext.replace("&nbsp", " ")
    return cleantext


def remove_von(value):
    return value.replace("Von ", "")


def remove_new_line(value):
    return value.replace("\xad", "")


def prep_kn_content(raw_content_data: Dict[str, str]) -> Dict[str, str]:
    prep_content_data = {}

    for key, value in raw_content_data["content"].items():
        if type(value) == str:
            value = cleanhtml(value)
            value = remove_new_line(value)
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
