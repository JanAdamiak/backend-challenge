"""
This script allows the user to output a JSON file based on the data of 2 csv files.
Currently the outputted JSON file is saved locally, which is not ideal.
Since data transformation is generally quite slow, this should be ran as a CronJob and not on demand REST API.

A good practice would be to save this JSON file to an object storage, that authorised users can later read or consume with a REST API or save in cache.
"""

from utils import json_outputter


def run():
    """
    main function
    """
    json_outputter()


if __name__ == "__main__":
    run()
