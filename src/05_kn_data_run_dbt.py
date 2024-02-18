# -*- coding: utf-8 -*-
"""
KN-Data-DB-Upload

Step 5: Run DBT

Runs the dbt command to update the data to the Postgres DB

Usage:
    kn_data_db_upload.py

Example:
    python kn_data_db_upload.py

Author: Lukas Krabbe (mail@l-krabbe.de)

Copyright (c) 2023 Lukas Krabbe
"""
import os
import sys

from helpers.log import get_logger
from helpers.secrets import get_secret_from_env

from dbt.cli.main import dbtRunner

logger = get_logger("run_dbt")

cwd = os.getcwd()
os.chdir(cwd + "/dbt")

def main(param: list):
    """
    Main function for the KN-Data-Upload

    Args:
        param: List of arguments passed to the script

    Returns:

    """
    logger.info("Start DBT Run")

    # initialize
    dbt = dbtRunner()

    secret = get_secret_from_env("POSTGRESDB_USER_SECRET", '../secrets/')
    # create CLI args as a list of strings
    os.environ["DBT_USER"] = secret['user']
    os.environ["DBT_PASSWORD"] = secret['password']
    cli_args = ["run"]

    # run the command
    dbt.invoke(cli_args)

    # inspect the results
    # for r in res.result:
    #     print(f"{r.node.name}: {r.status}")

    logger.info("Finished DBT Run")


if __name__ == "__main__":
    main(sys.argv)
