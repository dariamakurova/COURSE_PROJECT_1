import datetime
import json
import os

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.reports import excel_creator_default, excel_creator_filename, spending_by_category, report_spending_by_category


def test_spending_by_category(testing_transactions_categories):
    transactions = pd.DataFrame(testing_transactions_categories)
    date = "2018-02-01 00:00:00"

    result = spending_by_category(transactions, category="Красота", date=date)

    assert isinstance(result, pd.DataFrame)
    assert all(result["Категория"] == "Красота")

    end_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_date = end_date - relativedelta(months=3)
    for date_str in result["Дата операции"]:
        operation_date = datetime.datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
        assert start_date <= operation_date <= end_date


def test_excel_creator_default():
    @excel_creator_default
    def func():
        df = pd.DataFrame({"Операция": ["Покупка", "Перевод", "Покупка"], "Сумма": [200, 350, 561]})
        return df

    result = func()
    assert os.path.exists(result)


def test_excel_creator_filename():
    @excel_creator_filename(filename="тест")
    def func():
        df = pd.DataFrame({"Операция": ["Покупка", "Перевод", "Покупка"], "Сумма": [200, 350, 561]})
        return df

    result = func()
    assert os.path.exists(result)
    assert result.endswith("тест.xlsx")


def test_report_spending_by_category():
    df = pd.DataFrame({"Операция" : ["Покупка", "Перевод", "Покупка"], "Сумма" : [200, 350, 561]})
    report = json.loads(report_spending_by_category(df))
    assert df.shape[0] == len(report)
