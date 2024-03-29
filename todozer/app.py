#!/usr/bin/env python3

import os
from sys import stdout

import click

from todozer import constants
from todozer.commands import command_beep, command_make, command_show, command_test


def __get_path(path: str | None) -> str:
    """
    Determines the path to a working directory. It is supposed to be the "Todozer" folder
    in user's home directory in case it's not specified via app's options.
    """

    if path is None:
        path = os.path.expanduser("~")
        path = os.path.join(path, "Todozer")

    return path


def __path_help() -> str:
    return "Set path to working directory."


def __path_type() -> click.Path:
    return click.Path(exists=True)


@click.group(help="CLI tool to manage tasks & duties.")
def cli():
    stdout.reconfigure(encoding=constants.ENCODING)


@cli.command(help="Make planned tasks for a brand-new day.")
@click.option("-p", "--path", type=__path_type(), help=__path_help())
def make(path: str | None) -> None:
    path = __get_path(path)
    command_make.main(path)


@cli.command(help="Check that data files have no mistakes.")
@click.option("-p", "--path", type=__path_type(), help=__path_help())
def test(path: str | None) -> None:
    path = __get_path(path)
    command_test.main(path)


@cli.command(help="Set alarm according to notification settings.")
@click.option("-p", "--path", type=__path_type(), help=__path_help())
def beep(path: str | None):
    path = __get_path(path)
    command_beep.main(path)


@cli.command(help="Display tasks for a given day (or days).")
@click.argument(
    "period", default="today", type=click.Choice(["today", "last", "next", "date"])
)
@click.argument("value", default="")
@click.option("-p", "--path", type=__path_type(), help=__path_help())
@click.option(
    "-t", "--timesheet", is_flag=True, help="Show only tasks with time logged."
)
@click.option("-l", "--logs", is_flag=True, help="Show time logged for each task.")
def show(path: str | None, timesheet: bool, logs: bool, period: str, value: str):
    path = __get_path(path)
    command_show.main(period, value, path, timesheet, logs)


if __name__ == "__main__":
    cli()
