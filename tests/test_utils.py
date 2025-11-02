from math import nan
from unittest.mock import patch

import pytest
from dotenv import load_dotenv
import os

from src.utils import get_cashback, get_greeting, get_last_digits, get_top_5_by_spent, get_total_spent, \
    get_currency_rates, get_stock_price, open_excel


# тесты для get_greeting()


def test_get_greeting_night():
    assert get_greeting("2025-06-23 02:33:54") == "Доброй ночи"


def test_get_greeting_morning():
    assert get_greeting("2025-06-23 11:59:59") == "Доброе утро"


def test_get_greeting_day():
    assert get_greeting("2025-06-23 15:05:00") == "Добрый день"


def test_get_greeting_evening():
    assert get_greeting("2025-06-23 19:06:10") == "Добрый вечер"


# тесты для get_last_digits()


def test_get_last_digits(testing_transactions):
    assert get_last_digits(testing_transactions) == ["7197", "5814"]


# тесты для get_total_spent()


def test_get_total_spent(testing_transactions):
    assert get_total_spent(testing_transactions, "7197") == 5043.75


# тесты для get_cashback()


def test_get_cashback():
    assert get_cashback(1856.87) == 18.57
    assert get_cashback(0) == 0
    assert get_cashback(None) == 0


# тесты для get_top_5_by_spent()


def test_get_top_5_by_spent(testing_transactions):
    assert get_top_5_by_spent(testing_transactions) == [
        {
            "amount": -3089.97,
            "category": "Одежда и обувь",
            "date": "11.01.2018",
            "description": "Veikals Rosme, Mukusalas",
        },
        {"amount": -3000.0, "category": "Переводы", "date": "01.01.2018", "description": "Линзомат ТЦ Юность"},
        {"amount": -1574.59, "category": "Супермаркеты", "date": "12.01.2018", "description": "Rimi Hm Gramzdas"},
        {"amount": -316.0, "category": "Красота", "date": "01.01.2018", "description": "OOO Balid"},
        {"amount": -191.13, "category": "Топливо", "date": "10.01.2018", "description": "Circle K"},
    ]

# тесты для get_currency_rates()

def test_get_currency_rates():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {'result': 'success',
                                                   'documentation': 'https://www.exchangerate-api.com/docs',
                                                   'terms_of_use': 'https://www.exchangerate-api.com/terms',
                                                   'time_last_update_unix': 1761436802,
                                                   'time_last_update_utc': 'Sun, 26 Oct 2025 00:00:02 +0000',
                                                   'time_next_update_unix': 1761523202,
                                                   'time_next_update_utc': 'Mon, 27 Oct 2025 00:00:02 +0000',
                                                   'base_code': 'USD', 'conversion_rates':
                                                       {'USD': 1, 'AED': 3.6725, 'AFN': 66.2253, 'ALL': 83.0727,
                                                        'AMD': 382.1194, 'RUB': 81.79, 'AOA': 921.3158, 'ARS': 1485.92}}

        load_dotenv()
        EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
        API_KEY = EXCHANGE_API_KEY
        assert get_currency_rates("USD") == 81.79
        mock_get.assert_called_once_with(f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD')


# тесты для get_stock_price()

def test_get_stock_price():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {'c': 269.7, 'd': 0.7, 'dp': 0.2602, 'h': 271.41, 'l': 267.11,
                                                   'o': 269.275, 'pc': 269, 't': 1761768000}
        load_dotenv()
        SP500_API_KEY = os.getenv("SP500_API_KEY")
        API_KEY = SP500_API_KEY
        assert get_stock_price("AAPL") == 269.7
        mock_get.assert_called_once_with(f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={API_KEY}")


# тесты для open_excel

def test_open_excel():
    path = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "Transactions_test_mini.xlsx")
    assert open_excel(path) == [{'Дата платежа': '31.12.2021', 'Номер карты': '*7197', 'Статус': 'OK',
                                 'Сумма операции': -160.89, 'Валюта операции': 'RUB'},
                                {'Дата платежа': '31.12.2021', 'Номер карты': '*5091', 'Статус': 'OK',
                                 'Сумма операции': -564.0, 'Валюта операции': 'RUB'},
                                {'Дата платежа': '30.12.2021', 'Номер карты': '*4556', 'Статус': 'OK',
                                 'Сумма операции': 5046.0, 'Валюта операции': 'RUB'},
                                {'Дата платежа': '30.12.2021', 'Номер карты': '*7197', 'Статус': 'OK',
                                 'Сумма операции': -349.0, 'Валюта операции': 'RUB'},
                                {'Дата платежа': '14.11.2021', 'Номер карты': '*4556', 'Статус': 'FAILED',
                                 'Сумма операции': -55.0, 'Валюта операции': 'RUB'}]
    path_log = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "utils.log")
    with open(path_log, "r") as f:
        result = f.read()
        assert "Чтение данных из файла" in result

def test_open_excel_empty():
    path = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "Empty.xlsx")
    assert open_excel(path) == []


def test_open_excel_no_file():
    path = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "No_file.xlsx")
    assert open_excel(path) == []
    path_log = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "utils.log")
    with open(path_log, "r") as f:
        result = f.read()
        assert "Файл не найден" in result



def test_open_excel_failed():
    fake_file = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "fake.xlsx")
    with open (fake_file, 'w') as f:
        f.write("ерунда какая-то")

    with patch('src.utils.pd.read_excel', side_effect=ValueError("Ошибка чтения файла")):
        result = open_excel(fake_file)
        assert result == []
