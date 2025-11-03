import datetime
import json
import os

from src.utils import get_greeting, get_cards_info, open_excel, get_top_5_by_spent, get_currency_rates_list, \
    get_stocks_prices_list


def views(date: str) -> str:
    """ Функция главной страницы, которая принимает на вход дату в формате YYYY-MM-DD HH:MM:SS
    возвращает json строку с данными на указанную дату"""

    greeting = get_greeting(date)

    transactions_xlsx = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "operations.xlsx")
    transactions = open_excel(transactions_xlsx)

    user_settings_file = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "user_settings.json")

    data_str = {
        "greeting": greeting,
        "cards": get_cards_info(transactions),
        "top_transactions": get_top_5_by_spent(transactions),
        "currency_rates": get_currency_rates_list(user_settings_file),
        "stock_prices": get_stocks_prices_list(user_settings_file)
    }

    data_json = json.dumps(data_str, sort_keys=False, indent=4, ensure_ascii=False)

    return data_json

if __name__ == "__main__":

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(views(date))