import os
import pickle

from loguru import logger as log
from yaml import safe_load


def get_flowers_to_collected(config):
    flowers = [f for f, v in config.items() if v["enabled"]]
    if not flowers:
        log.error("No flowers found in config file")
        exit(1)
    return flowers


def create_dump_path(dump_path):
    if not os.path.exists(dump_path):
        try:
            log.debug("Create dump directory")
            os.makedirs(dump_path)
        except Exception as e:
            log.error(f"The dump directory cannot be created: {e}")
            exit(1)


def get_config(conf_file):
    log.debug(f"Get yaml config file: {conf_file}")
    try:
        with open(conf_file) as f:
            data = safe_load(f)
        return data["configs"]
    except FileNotFoundError as e:
        log.error(f"The config file was not found: {e}")
        exit(1)
    except Exception as e:
        log.error(f"The config file cannot be parsed: {e}")
        exit(1)


def write_dump_data_to_file(dump_file, data):
    log.debug(f"Write dump data to {dump_file} ..")
    with open(dump_file, "wb+") as f:
        pickle.dump((data, ), f, pickle.HIGHEST_PROTOCOL)


def read_dump_data_from_file(dump_file):
    log.debug(f"Read dump data from {dump_file} ..")
    with open(dump_file, "rb") as f:
        data = pickle.load(f)[0]
    return data