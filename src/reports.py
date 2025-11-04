import datetime
import json
import logging

from dateutil.relativedelta import relativedelta
import os
from typing import Optional

import pandas as pd

from src.utils import transfer_into_dataframe, open_excel

reports_logger = logging.getLogger("reports_logger")
logger_file = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "reports.log")
reports_handler = logging.FileHandler(logger_file, mode="w")
reports_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
reports_handler.setFormatter(reports_formatter)
reports_logger.addHandler(reports_handler)
reports_logger.setLevel(logging.DEBUG)


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    reports_logger.info("Формирование временного периода для отчета")
    if date:
        end_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    else:
        end_date = datetime.datetime.now()

    start_date = end_date - relativedelta(months=3)

    transactions['Дата_операции_dt'] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    reports_logger.info("Поиск по операциям")
    sorted_transactions = transactions.loc[(transactions["Категория"] == category) &
                                           (start_date <= transactions["Дата_операции_dt"]) &
                                           (transactions["Дата_операции_dt"] <= end_date)]
    reports_logger.info("Список операций в заданной категории сформирован")

    return sorted_transactions


def report_spending_by_category(df: pd.DataFrame) -> str | None:
    """ Преобразование DF в json строку """

    sorted_transactions_json = df.to_json(orient="records", force_ascii=False)
    return sorted_transactions_json


if __name__ == "__main__":

    transactions_xlsx = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "operations.xlsx")
    all_transactions = open_excel(transactions_xlsx)
    transactions = transfer_into_dataframe(all_transactions)
    print(spending_by_category(transactions, "Красота","2019-03-20 00:00:00"))