import json

from black import datetime
import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd

from src.reports import spending_by_category


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


