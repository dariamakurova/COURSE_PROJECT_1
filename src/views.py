import datetime

from src.utils import get_greeting


def views(date: datetime) -> str:
    """ Функция главной страницы, которая принимвет на вход дату в формате YYYY-MM-DD HH:MM:SS
    возвращает json строку с данными на указанную дату"""

    greeting = get_greeting(date)

    data_str = {
        "greeting": greeting
    }