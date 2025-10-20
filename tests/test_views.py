
from src.views import get_greeting

# тесты для get_greeting()

def test_get_greeting_night():
    assert get_greeting("2025-06-23 02:33:54") == "Доброй ночи"


def test_get_greeting_morning():
    assert get_greeting("2025-06-23 11:59:59") == "Доброе утро"


def test_get_greeting_day():
    assert get_greeting("2025-06-23 15:05:00") == "Добрый день"


def test_get_greeting_evening():
    assert get_greeting("2025-06-23 19:06:10") == "Добрый вечер"