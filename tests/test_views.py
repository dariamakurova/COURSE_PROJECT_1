from math import nan

from src.views import get_cashback, get_greeting, get_last_digits, get_top_5_by_spent, get_total_spent

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


# тесты для get_cashback


def test_get_cashback():
    assert get_cashback(1856.87) == 18.57
    assert get_cashback(0) == 0
    assert get_cashback(None) == 0


# тесты для get_top_5_by_spent


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
