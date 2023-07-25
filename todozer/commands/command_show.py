#!/usr/bin/env python3

"""Simply outputs tasks for a given date and quits."""

import datetime

import click

from todozer import state_file, task_lists, utils
from todozer.todo import list_todo


def main(period: str, value: str, path: str | None, timesheet: bool) -> None:
    """
    Checks plans file for errors.
    """

    config = utils.get_config(path)
    utils.set_logging(config)

    state = state_file.load(path)

    tasks = task_lists.load_tasks_file_items(config, path)
    plans = task_lists.load_plans_file_items(config, path)

    if period == "today":
        __show_today(tasks, plans, state, timesheet)
    elif period == "last":
        __show_last_n_days(tasks, plans, state, int(value) if value else 1, timesheet)
    elif period == "next":
        __show_next_n_days(tasks, plans, state, int(value) if value else 1, timesheet)
    elif period == "date":
        __show_date(tasks, plans, state, value, timesheet)


def __show_today(tasks, plans, state, timesheet) -> None:
    date = utils.get_date_of_today()
    __print_tasks_by_date(date, tasks, plans, state, timesheet)
    click.echo()


def __show_last_n_days(tasks, plans, state, days_number: int, timesheet) -> None:
    date = utils.get_date_of_today() - datetime.timedelta(days=days_number)
    for _ in range(days_number):
        __print_tasks_by_date(date, tasks, plans, state, timesheet)
        date += datetime.timedelta(days=1)
        click.echo()


def __show_next_n_days(tasks, plans, state, days_number: int, timesheet) -> None:
    date = utils.get_date_of_today()
    for _ in range(days_number):
        date += datetime.timedelta(days=1)
        __print_tasks_by_date(date, tasks, plans, state, timesheet)
        click.echo()


def __show_date(tasks, plans, state, date: str, timesheet) -> None:
    date = utils.get_date_from_string(date)
    __print_tasks_by_date(date, tasks, plans, state, timesheet)
    click.echo()


def __print_tasks_by_date(date, tasks, plans, state, timesheet) -> None:
    title = utils.get_string_from_date(date)

    click.echo(f"# {title}")
    click.echo()

    tasks_list = task_lists.get_tasks_list_by_date(tasks, date)

    if tasks_list is None:
        tasks.append(list_todo.ListTodo(f"# {title}"))
        tasks_list = tasks[-1]

    if date > state["last_planning_date"]:
        task_lists.fill_tasks_list(tasks_list, plans)

    if tasks_list.items:
        for task in tasks_list.items:
            timer_string = task.timer_string
            if timesheet:
                if not timer_string:
                    continue

            if timer_string != "":
                timer_string = f" ({timer_string})"

            click.echo(f"{task.title_line}{timer_string}")

    else:
        click.echo("No tasks found.")


if __name__ == "__main__":
    main(what="today", detail="", path=None, time=False)
