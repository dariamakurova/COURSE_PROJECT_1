import datetime
import json
import os

from src.utils import (get_cards_info, get_currency_rates_list, get_greeting, get_stocks_prices_list,
                       get_top_5_by_spent, get_transactions_for_period, open_excel)


def views_main(date: str) -> str:
    """Функция главной страницы, которая принимает на вход дату в формате YYYY-MM-DD HH:MM:SS
    возвращает json строку с данными на указанную дату"""

    greeting = get_greeting(date)

    transactions_xlsx = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "operations.xlsx")
    all_transactions = open_excel(transactions_xlsx)
    transactions = get_transactions_for_period(date, all_transactions)

    user_settings_file = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "user_settings.json")

    data_str = {
        "greeting": greeting,
        "cards": get_cards_info(transactions),
        "top_transactions": get_top_5_by_spent(transactions),
        "currency_rates": get_currency_rates_list(user_settings_file),
        "stock_prices": get_stocks_prices_list(user_settings_file),
    }

    data_json = json.dumps(data_str, sort_keys=False, indent=4, ensure_ascii=False)

    return data_json


if __name__ == "__main__":

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(views_main(date))
