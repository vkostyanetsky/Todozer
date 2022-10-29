#!/usr/bin/env python3

"""Methods to read and write the app's state file."""

import os

import yaml
import yaml.parser

from todozer import constants, utils


def save_yaml(file_name: str, file_data: dict) -> None:
    """Writes a dictionary as a YAML file."""

    with open(file_name, encoding=constants.ENCODING, mode="w") as yaml_file:
        yaml.safe_dump(file_data, yaml_file)


def load_yaml(file_name: str) -> dict:
    """Reads a YAML file as a dictionary."""

    result = None

    try:

        with open(file_name, encoding=constants.ENCODING) as yaml_file:
            result = yaml.safe_load(yaml_file)

    except yaml.parser.ParserError:
        print(f"Unable to parse {file_name}!")

    if result is None:
        result = {}

    return result


def get_data_file_name() -> str:
    """Returns the app's data file name."""

    return "todozer.dat"


def get_data_by_default() -> dict:
    """Returns default app's data."""

    return {
        "last_planning_date": utils.get_date_of_yesterday(),
        "running_timer_date": None,
    }


def load() -> dict:
    """Returns the app's data."""

    file_name = get_data_file_name()

    return load_yaml(file_name) if os.path.exists(file_name) else get_data_by_default()


def save(data: dict):
    """Writes the app's data."""

    file_name = get_data_file_name()

    save_yaml(file_name, data)