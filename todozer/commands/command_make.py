#!/usr/bin/env python3

"""Creates planned tasks for today (and days before, if it is required)."""

import logging

from todozer import echo, state_file, task_lists, utils


def main(path: str) -> None:
    """
    Creates tasks for the today (and days before, in case it was not done yet).

    All tasks in progress must be marked as completed or rearranged
    to other upcoming date before the user runs the procedure.
    """

    config = utils.get_config(path)
    utils.set_logging(config)

    logging.debug("Creating planned tasks...")

    state = state_file.load(path)

    tasks_file_items = task_lists.load_tasks_file_items(config, path)
    plans_file_items = task_lists.load_plans_file_items(config, path)

    task_lists.add_tasks_lists(tasks_file_items, state["last_planning_date"])

    if check_for_tasks_in_progress(tasks_file_items):
        filled_list_titles = task_lists.fill_tasks_lists(
            tasks_file_items, plans_file_items, state
        )

        if filled_list_titles:
            task_lists.save_tasks_file_items(tasks_file_items, config, path)

            state["last_planning_date"] = utils.get_date_of_today()

            __clean_triggered_notifications(state)

            state_file.save(path, state)

            scheduled_tasks = ", ".join(filled_list_titles)

            echo.success(f"Tasks for {scheduled_tasks} have been successfully created.")

        else:
            echo.warning(
                "At this point, everything is planned, so there is nothing to make."
            )

        echo.line()


def check_for_tasks_in_progress(tasks_file_items: list) -> bool:
    passed = True

    dates_in_progress = task_lists.get_task_lists_in_progress(tasks_file_items)

    if dates_in_progress:
        passed = False

        echo.warning("Unable to perform, since there is at least one task in progress:")
        echo.line()

        for date_in_progress in dates_in_progress:
            echo.warning(date_in_progress)
            echo.warning()

        echo.warning(
            "You have to rearrange tasks in progress or mark them as completed."
        )

    return passed


def __clean_triggered_notifications(state) -> None:
    date_strings = list(state["triggered_notifications"].keys())

    for date_string in date_strings:
        if utils.get_date_from_string(date_string) < state["last_planning_date"]:
            del state["triggered_notifications"][date_string]


if __name__ == "__main__":
    main(path="")
