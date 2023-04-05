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


def split_mulitple_authors(value):
    value = value.replace(" und ", ", ")
    value = value.replace("und ", ", ")
    value = value.replace("UND ", ", ")
    value = value.replace(" UND ", ", ")

    if ", " in value:
        value = value.split(", ")
        tmp = {}
        for i, val in enumerate(value):
            tmp[f"author_{i}"] = val
        return tmp
    else:
        return {"author_0": value}


def remove_city(value):
    match = re.search(r"^ [A-züäö\/A-züäö]*\. ", value)
    if match:
        city = value[match.start() : match.end()]
        text = value[len(city) :]
        city = city.replace(" ", "")
        city = city.replace(".", "")
        if "/" in city:
            city = city.split("/")[0]
        city = city.lower().title()

        if city.lower() in [
            "montag",
            "dienstag",
            "mittwoch",
            "donnerstag",
            "freitag",
            "samstag",
            "sonntag",
        ]:
            city = None

    else:
        text = value
        city = None

    return text, city


def prep_kn_content(raw_content_data: Dict[str, str]) -> Dict[str, str]:
    prep_content_data = {}

    for key, value in raw_content_data["content"].items():
        if type(value) == str:
            value = cleanhtml(value)
            value = remove_new_line(value)
            value = remove_multiple_spaces(value)
            if key == "author":
                value = remove_von(value)
                value = split_mulitple_authors(value)
                prep_content_data["author"] = {}
                for key, val in value.items():
                    prep_content_data["author"][key] = val
            if key == "page":
                value = int(value)
            if key == "body":
                if len(value) > 25:
                    value, city = remove_city(value)
                    if city:
                        prep_content_data["city"] = city

        if key in [
            "body",
            "title",
            "releaseDate",
            "page",
            "subtitle",
            "resort",
        ]:
            prep_content_data[key] = value

    return prep_content_data
