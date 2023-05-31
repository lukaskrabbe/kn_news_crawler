# -*- coding: utf-8 -*-
import logging

import psycopg2
import pymongo
from helpers.secrets import get_secret_from_env

logger = logging.getLogger("secrets")


def get_posgtres_connection():
    """
    Get a connection to the Postgres DB

    Returns:
        conn: Connection to the Postgres DB
    """
    secret = get_secret_from_env("POSTGRESDB_USER_SECRET", path="../secrets/")

    conn = psycopg2.connect(
        host="81.169.252.177",
        port="5432",
        user=secret["user"],
        password=secret["password"],
        database="kn",
    )
    logger.info("Connected to Postgres DB")

    return conn


def get_mongo_connection():
    """
    Get a connection to the MongoDB kn_db.kn_data collection

    Returns:

    """
    secret = get_secret_from_env("MONGO_USER_SECRET", path="../secrets/")

    mongo_client = pymongo.MongoClient(
        f"mongodb://{secret['user']}:{secret['password']}@81.169.252.177:27017/?authMechanism=DEFAULT&tls=false"
    )
    kn_db = mongo_client.kn_db
    kn_collection = kn_db.get_collection("kn_data")

    assert len(kn_collection.find_one({})) > 0, "Error, no Data or DB-Connection"
    logger.info("Connected to MongoDB kn_db.kn_data collection")

    return kn_collection
