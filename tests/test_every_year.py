import datetime
import locale

import tests.helpers
import todozer.scheduler
import todozer.utils


def run_test_ru(
    result: bool, task_date: datetime.date, start_date: datetime.date = None
):

    locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

    task_date = task_date.strftime("%d %B")
    task_text = tests.helpers.get_task_text_ru(f"каждый год, {task_date}", start_date)

    today = todozer.utils.get_date_of_today()

    assert todozer.scheduler.match(task_text, today) is result


def run_test_en(
    result: bool, task_date: datetime.date, start_date: datetime.date = None
):

    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    task_date = task_date.strftime("%B %d")
    task_text = tests.helpers.get_task_text_ru(f"every year, {task_date}", start_date)

    today = todozer.utils.get_date_of_today()

    assert todozer.scheduler.match(task_text, today) is result


def test_every_year():

    yesterday = todozer.utils.get_date_of_yesterday()
    tomorrow = todozer.utils.get_date_of_tomorrow()
    today = todozer.utils.get_date_of_today()

    # ru

    run_test_ru(result=True, task_date=today)
    run_test_ru(result=True, task_date=today, start_date=yesterday)
    run_test_ru(result=False, task_date=today, start_date=tomorrow)

    run_test_ru(result=False, task_date=tomorrow)
    run_test_ru(result=False, task_date=tomorrow, start_date=yesterday)
    run_test_ru(result=False, task_date=tomorrow, start_date=tomorrow)

    # en

    run_test_en(result=True, task_date=today)
    run_test_en(result=True, task_date=today, start_date=yesterday)
    run_test_en(result=False, task_date=today, start_date=tomorrow)

    run_test_en(result=False, task_date=tomorrow)
    run_test_en(result=False, task_date=tomorrow, start_date=yesterday)
    run_test_en(result=False, task_date=tomorrow, start_date=tomorrow)
